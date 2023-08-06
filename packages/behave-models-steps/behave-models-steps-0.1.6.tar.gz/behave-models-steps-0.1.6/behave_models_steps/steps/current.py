from inflection import titleize, pluralize, camelize, singularize
import importlib
import inspect
from behave import *
from faker import Faker
import random
from hamcrest import *
from freezegun import freeze_time
from ..utils import *

LocalData = LocalDataClass()

use_step_matcher("re")
faker = Faker()

# from app.helpers.UUIDgenerator import UUIDGenerator, LocalData.UUID
# from app.helpers.model_helpers import redo_attrs, REDO_ATTR_IN_MODELS

# from test_data.model_constants import *

# ----- USED IN MODEL __init__ TESTING ----- #
freezer = freeze_time("2012-01-14 12:00:01")
#  ===== ACTUAL STEPS =====   #


@when(u'I create a new "(?P<creatable_type>.*)" named "(?P<type_name>\w+)"(?P<_maybe_belong_> belonging to )?'
      u'(?P<owner_type_>\w+ )?(?P<owner_name>".*")?')
def step_impl(context, creatable_type, type_name, _maybe_belong_, owner_type_, owner_name):
    context.model = load_class('app.models.', creatable_type)

    if _maybe_belong_:
        owner_klass = load_class('app.models.', owner_type_.strip())
        owner = owner_klass(owner_name)
        model_to_check = context.model(type_name, owner)
    else:
        model_to_check = context.model(type_name)

    with LocalData.app.app_context():
        LocalData.db.session.add(model_to_check)
        LocalData.db.session.commit()
        context.owner = owner_klass.query.filter_by(name=owner_name).one()
        setattr(context, creatable_type, context.model.query.filter_by(name=type_name).one())
        context.model_to_check = context.model.query.filter_by(name=type_name).one()


@then(u'the "(?P<creatable_type>.*)" will have(?P<_a_type> a type)? (?:")?(?P<extra_attr_type>\w+)(?:")?'
      u' "(?P<extra_attr_value>.*)"')
def step_impl(context, creatable_type, _a_type, extra_attr_type, extra_attr_value):
    with LocalData.app.app_context():
        if _a_type:
            if extra_attr_type == 'str':
                myvalue = getattr(getattr(context, creatable_type), extra_attr_value).encode('utf-8')
            else:
                myvalue = getattr(getattr(context, creatable_type), extra_attr_value)
            assert_that(isinstance(myvalue, eval(extra_attr_type)))
        else:
            if extra_attr_type in LocalData.reencode:
                myvalue = getattr(getattr(context, creatable_type), extra_attr_type).encode('utf-8')
            else:
                myvalue = getattr(getattr(context, creatable_type), extra_attr_type)
            assert_that(myvalue, equal_to(extra_attr_value))


@then(u'the "(?P<creatable_type>.*)" will belong to (?P<owner_type>\w+) "(?P<owner_name>.*)"')
def step_impl(context, creatable_type, owner_type, owner_name):
    assert_that(getattr(getattr(context, creatable_type), owner_type).name, owner_name)


# ----- USED IN model_helpers AND ALL __init__ tests ----- #

@given(u'I(?: do)?(?P<_or_not>n\'t)? want to create a(?:n)? "(?P<model_type>.*)"')
def step_impl(context, _or_not, model_type):
    """
    This step will tell us whether or not to persist the model we are checking
    """
    freezer.start()

    setattr(context, model_type + '_persisted', _or_not != 'n\'t')
    context.model = load_class('app.models.', model_type)


@given(u'a(?:n)? (?P<owner_type>\w+) exists in the db(?P<add_client> belonging to client "(?P<clientname>.*)")?')
def step_impl(context, owner_type, add_client, clientname):
    """
    The model has to be owned by a specific type of other model (i.e. owned by group/client)
    """
    from app.models.clients import Client
    owner_attrs = {}
    if add_client:
        owner_klass = load_class('app.models.', owner_type)
        client = Client(clientname)
        if owner_type == 'user':
            owner_attrs = {'nickname': faker.user_name(), 'email': faker.email(), 'client': client}
        elif owner_type == 'user_group':
            owner_attrs = {'name': faker.catch_phrase(), 'client': client}
    if owner_type == 'client':
        owner_klass = Client
        owner_attrs = {'name': faker.company()}

    with LocalData.app.app_context():
        LocalData.db.session.add(owner_klass(**owner_attrs))
        LocalData.db.session.commit()
        owner_attrs.pop('client', None)
        context.owner_obj = owner_klass.query.filter_by(**owner_attrs).one()

    context.owner = owner_type


@given(u'this "(?P<model_type>.*)" (?P<does_or_not>has|does not have) (?:required )?option (?P<attr_name>\w+)'
       u'(?: with a(?:n)? (?P<appender>\w+))?(?: "(?P<attr_value>.*)")?')
def step_impl(context, model_type, does_or_not, attr_name, attr_value, appender):
    """
    Build up a dictionary in context.<modelname>_attrs that will hold all the necessary create_method args
    for the model we want to create
    """
    # print "HAS REQD OPTION?", model_type, does_or_not, attr_name, attr_value, appender
    reset_attr = False  # used to reset he attr_name and stick a "_" back in front of it
    if does_or_not != 'does not have':
        try:
            temp_attrs = getattr(context, model_type + '_attrs')
        except AttributeError:
            temp_attrs = {}

        # we want to make sure to have the correct attr_name, sometimes we have private attrs that we
        # reference in the __init__ as non-private (i.e. Class._value but in __init__ we have value=)
        if private_attr(attr_name):
            optional_args, required_args = init_args(context.model)
            model_args = (optional_args + required_args)
            if attr_name not in model_args and attr_name[1:] in model_args:  # always assume it's just ONE underscore
                attr_name = attr_name[1:]
                reset_attr = True

        if appender:
            attr_name = 'group' if attr_name == 'user_group' else attr_name
            temp_attrs[attr_name + '_' + appender.lower()] = getattr(context.owner_obj, appender.lower())
        else:
            # print "ORIG ATTR", attr_value, '\n', context
            # backward compatible, as it simply returns the value if not type prepended
            attr_value = make_attr(attr_value, attr_name, model_type, context)
            # print "AFTER MANIP:", attr_value, "FOR", context.model
            temp_attrs[attr_name] = attr_value

            # Create the relation model if it requires one for the specific attribute
            if attr_name in LocalData.RELATIONS_NOT_FIELDS and is_primative(attr_value):
                klass_args, make_klass = create_non_primative(attr_name, attr_value)
                # print "GOING TO MAKE SPECIAL CLASS RELATION:", make_klass, "\nWITH:", klass_args
                temp_attrs[attr_name] = make_klass(**klass_args)

        if reset_attr:
            temp_attrs['_' + attr_name] = temp_attrs[attr_name]
            temp_attrs.pop(attr_name)
        setattr(context, model_type + '_attrs', temp_attrs)
        # import pprint
        # pprint.pprint(temp_attrs)


@given(u'this "(?P<model_type>.*)" (?P<not_>does not )?belong(?:s)? to (?P<owner_type>\w+) "(?P<owner_name>.*)"')
def step_impl(context, model_type, not_, owner_type, owner_name):
    """
    A step to provide ownership of this model to another model
    """
    if not not_:
        setattr(context, model_type + '_owner_type', owner_type)
        setattr(context, model_type + '_owner_name', owner_name)


@given(u'this "(?P<model_type>.*)" needs to be re-persisted(?P<_db> to the db)?')
def step_impl(context, model_type, _db):
    with LocalData.app.app_context():
        try:
            LocalData.db.session.add(getattr(context, 'desired_' + model_type))
        except:
            print "ALREADY EXISTS IN SESSION"
        LocalData.db.session.commit()
        # from app import pp
        # print "AFTER PERSISTING:"
        # pp.pprint(getattr(context, 'desired_' + model_type).__dict__)


@given(u'this "(?P<model_type>.*)" is(?:n\'t)? persisted(?P<_db> to the db)?')
def step_impl(context, model_type, _db):
    """
    The step used to save the model itself in the db
    """
    untouched_attrs = getattr(context, model_type + '_attrs')
    if 'owner' in context:  # if we've set an owner to this model
        untouched_attrs[context.owner] = context.owner_obj
        setattr(context, model_type + '_attrs' + '.' + context.owner, context.owner_obj)

    # remove empty (or null values)
    untouched_attrs = {k: v for k, v in untouched_attrs.items() if
                       v != ''}  # want strict empty string rather than falsey

    # now we want to remove any relations, rather than creation (init) keys
    negative_keys = ('groups', 'password') + LocalData.NON_OWNER_RELATIONS
    model_attrs = {k: v for k, v in untouched_attrs.items() if k not in negative_keys}

    # print "UT", untouched_attrs

    if _db:
        with LocalData.app.app_context():
            # print "UNTOUCHED", untouched_attrs
            # load any relations so we can test against it to context.desired_<modelname>_<relation>
            # when a relation is loaded, we have a bool at context.check_relation
            for relation in [r for r in LocalData.NON_OWNER_RELATIONS if r in untouched_attrs.keys() and r != 'owner']:
                load_model_relation(context, relation, model_type)
                untouched_attrs[relation] = getattr(context, 'desired_' + model_type + '_' + relation)
                # print "MORE UNTOUCHED:", untouched_attrs[relation]
            # create the model we're testing (the ModelHelper will pop unnecessary keys)
            # print "UNTCOUHED", untouched_attrs
            try:
                temp_model, _ = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, context.model, **untouched_attrs)
            except Exception as ex:
                setattr(context, 'insert_error', type(ex))
                # raise ex

            # print "TEMP?", temp_model

            # only persist if we request
            if getattr(context, model_type + "_persisted") and not hasattr(context, 'insert_error'):
                model_attrs = LocalData.redo_attrs(context.model, {key: value for key, value in model_attrs.iteritems()
                                                         if not private_attr(key) and value})
                # print "MODEL_ATTRS", model_attrs
                # save the model to context.desired_<modelname>
                setattr(context, 'desired_' + model_type, context.model.query.filter_by(**model_attrs).one())
                # print getattr(context, 'desired_' + model_type)
                LocalData.db.session.commit()
            elif hasattr(context, 'insert_error'):
                setattr(context, 'desired_' + model_type, getattr(context, 'insert_error'))
            else:
                setattr(context, 'desired_' + model_type, temp_model)
    else:
        # no need to persist it, no after_insert or other ORM events required
        # print "UNTOUCHED", untouched_attrs, dict(map(lambda (k,v): (k, make_attr(v, k, model_type)), untouched_attrs))
        setattr(context, 'desired_' + model_type, context.model(**untouched_attrs))
        # print "MADE", getattr(context, 'desired_' + model_type)
        # import pprint
        # pprint.pprint(getattr(context, 'desired_' + model_type).__dict__)


@given(
    u'I set this "(?P<model_type>.*)"\'s "(?P<attr_name>.*)" using method "(?P<set_method>.*)"')  # (?: to be value )?("(?P<set_value>.*)")?')
def step_impl(context, model_type, attr_name, set_method):  # , set_value):
    """
    Set a specific attribute of a model using method <set_method> with optional value
    """
    # this is an optional step most of the time...
    if set_method:
        context.set_method = set_method
        set_method = model_method(context, set_method, model_type)
        # left here as we might want to implement this
        # if set_value:
        #     set_method(make_attr(set_value))
        # else:
        set_method()
        if getattr(context, model_type + "_persisted"):
            with LocalData.app.app_context():
                LocalData.db.session.commit()


@when(u'I request for this "(?P<model_type>.*)" with method "(?P<get_method>.*)" and arg "(?P<get_arg>.*)"')
def step_impl(context, model_type, get_method, get_arg):
    get_method = globals()[get_method]
    with LocalData.app.app_context():
        context.in_db = get_method(getattr(context, model_type + '_attrs')[get_arg])


@when(u'I request for this "(?P<model_type>.*)"\'s attribute "(?:.*)" with method "(?P<get_method>[\[\]\s\w\.\(\)]+)"'
      u'(?: and args "(?P<gargs>.*)")?')
def request_with_method_step(context, model_type, get_method, gargs):
    """
    Looking for a specific value either from an attribute or a method
    """
    context.get_method = get_method
    if hasattr(context, 'insert_error'):
        context.getter_value = getattr(context, 'insert_error')
    else:
        import pickle
        if gargs and is_method(gargs):
            gargs = make_method_from_string(context, gargs, model_type)
        # print "GET METHOD:", get_method
        # from app import pp
        # pp.pprint(getattr(context, 'desired_' + model_type).__dict__)
        # pp.pprint(getattr(getattr(context, 'desired_' + model_type), get_method))
        if child_of_method(get_method):
            method, submethod = get_method[5:-1].split('.')
            try:
                # assume that this is NOT a string and that it would work to submethod
                get_method = model_method(context, method, model_type).submethod
            except AttributeError:
                # this looks like we need to unpickle prior to submethod'ing
                get_method = getattr(pickle.loads(model_method(context, method, model_type)), submethod)
        elif single_pickled_instance(get_method):
            # print "SINGLE PICKLED", get_method[13:-1], getattr(context, 'desired_' + model_type, get_method[13:-1])
            get_method = pickle.loads(getattr(getattr(context, 'desired_' + model_type), get_method[13:-1]))
        elif unevaluated_and_namespaced(get_method) and not (get_method.startswith('[') and get_method.endswith(']')):
            pickled = True if get_method.startswith('pickle.loads(') else False
            relation, subrelation = get_method.split('.', 1) if not pickled else get_method[13:-1].split('.', 1)
            get_method = getattr(getattr(getattr(context, 'desired_' + model_type), relation), subrelation)
            if pickled:
                get_method = pickle.loads(get_method)
        elif get_method.startswith('[') and get_method.endswith(']'):  # want a list of relations (most likely)
            relation_name = get_method.split(']', 1)[0].split()[-1]
            if relation_name.startswith('pickle.loads('):
                import pickle
                relation = pickle.loads(request_with_method_step(context, model_type, relation_name[13:-1], None))
            elif unevaluated_and_namespaced(relation_name):
                get_from = getattr(context, 'desired_' + model_type)
                relation, subrelation = relation_name.split('.', 1)
                while '.' in subrelation:
                    get_from = getattr(get_from, relation)
                    relation, subrelation = subrelation.split('.', 1)
                relation = getattr(get_from, subrelation)
            else:
                relation = model_method(context, relation_name, model_type)
            setattr(context, 'list_relation', relation)
            # print "GETTING GET METHOD:", get_method, get_method.replace(relation_name, 'context.list_relation')
            get_method = eval(get_method.replace(relation_name, 'context.list_relation'))
        else:
            get_method = model_method(context, get_method, model_type)
        # print "THE ACTUAL METHOD IS:", get_method, gargs if gargs else ''
        try:
            # It's possible to have used callable to check, but decided to catch the error if it's an attribute
            with LocalData.app.app_context():  # often required to actually get from db
                context.getter_value = get_method() if not gargs else get_method(gargs)
        except TypeError:
            if getattr(context, model_type + "_persisted"):
                context.getter_value = get_method
                # import pickle
                # print "\nTHE GETTER:", pickle.loads(context.getter_value), "vs", getattr(context, 'desired_' + model_type)


@then(u'I expect this "(?P<model_type>.*)"\'s "(?P<attr_name>.*)" to be "(?P<get_value>.*)"')
def step_impl(context, model_type, attr_name, get_value):
    """
    This is where we check that the value is what we expect it to be
    """
    # make it into the attribute we want
    get_value = make_attr(get_value, attr_name, model_type)
    # if it's a LIST of models (i.e. a MANY-TO-MANY relationship), we need to make_attr again to get to keys
    if isinstance(get_value, list) and isinstance(get_value[0], dict):
        get_value = load_model_relation(context, attr_name, model_type, make_attr(get_value))
    elif isinstance(get_value, dict):
        get_value = load_model_relation(context, attr_name, model_type, get_value)
    # print "\nORIGINAL GET_VALUE", get_value, "\nCOMPARED TO", context.getter_value if context.getter_value else "NOT GOTTEN"
    # print context.get_method, attr_name, get_value, "IS ATTR_NAME IN MODEL?", attr_name in context.model.__dict__.keys(), "IS GETTER STR?", isinstance(context.getter_value, str)
    # if we're a relation, we have to create it as we would have earlier
    if attr_name == context.get_method and is_model_attribute(context.model, attr_name) \
        and attr_name in LocalData.RELATIONS_NOT_FIELDS and is_relations_list(get_value):
        klass_args, make_klass = create_non_primative(attr_name, get_value)
        with LocalData.app.app_context():
            # print "\nAttempting to import: ", attr_name, "WITH:", klass_args
            # we used the create_non_primative to check if we already have the object, if we do, make_klass is False
            if make_klass:
                attr = LocalData.relation_to_class[attr_name] if attr_name in LocalData.relation_to_class else attr_name
                get_value, _ = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, load_class('app.models.', attr), **klass_args)
            else:
                get_value = klass_args
                # print "ATTR", attr_name, get_value, "\nEXP:", get_value.experiments, "\n"
                # print "COMPARED", context.getter_value[0], "\nEXP:", context.getter_value[0].experiments, get_value in context.getter_value
                # print "IS IT FLUBBED GET_VALUE", get_value, "COMPARED TO", context.getter_value

    # need to hex the int version of that id so that it becomes a string
    if attr_name == 'LocalData.UUID' and isinstance(get_value, LocalData.UUID):
        get_value = LocalData.UUIDGenerator.LocalData.UUID_to_int(get_value.hex)
        context.getter_value = LocalData.UUIDGenerator.LocalData.UUID_to_int(context.getter_value)

    # print '\n\t', type(get_value), "\n\t", get_value.__dict__, '\n\tvs\n\t', context.getter_value.__dict__ if not isinstance(context.getter_value, list) else [c.__dict__ for c in context.getter_value]
    # assume that a non-primative means we may be missing some "after-insert" things
    if get_value and not is_primative(get_value) and not vanilla_object(get_value):
        if isinstance(get_value, list):
            pass
        elif isinstance(get_value, dict):
            pass
        elif hasattr(context, 'insert_error'):
            pass
        else:
            get_value = produce_comparable(context, get_value)
    # print '\n\t', type(get_value), "\n\t"
    # from app import pp
    # import pickle
    # pp.pprint(pickle.loads(get_value).__dict__)
    # pp.pprint(get_value.__dict__)
    # print 'vs\n\t'
    # print '\n\t', type(context.getter_value), "\n\t"
    # if isinstance(context.getter_value, list):
    #     print context.getter_value
    #     for gv in context.getter_value:
    #         print gv
    #         pp.pprint(gv.__dict__)
    # else:
    #     pp.pprint(context.getter_value.__dict__)

    # Expecting an error
    if hasattr(context, 'insert_error'):
        assert_that(getattr(context, 'insert_error'), equal_to(get_value))

    # print "\nIS ATTR_NAME", attr_name, " IN:", ('active', 'groups') + LocalData.NON_OWNER_RELATIONS
    if attr_name not in (('password', 'confirmed_at', 'active', 'groups', 'LocalData.UUID') + LocalData.NON_OWNER_RELATIONS):
        # we may ONLY care about existence of the object
        if isinstance(get_value, (str, unicode)) and get_value.startswith('exists='):
            assert_that(context.getter_value)
        else:
            assert_that(getattr(getattr(context, 'desired_' + model_type), attr_name), equal_to(get_value))

    # print "\nCHECK IF PERSISTENCE REQD", getattr(context, model_type + "_persisted"), "AND STR GETTER:", isinstance(context.getter_value, str)
    if getattr(context, model_type + "_persisted") and not hasattr(context, 'insert_error'):
        # print context.getter_value
        if isinstance(context.getter_value, str):
            import pickle
            # print "\nCG", type(context.getter_value), "\n\tGV", type(get_value)
            # it's very possible that we serialized a value into the DB, so let's try to deserialize it
            try:
                context.getter_value = pickle.loads(context.getter_value)
                # print "\nUNPICKLED:", context.getter_value, pickle.loads(context.getter_value)
            except (KeyError, EOFError, IndexError, ImportError):
                pass
        # print "\nCHECKING\n\t", [c.form for c in context.getter_value], "\n\tAGAINST\n\t", get_value.form
        if (attr_name in LocalData.RELATIONS_NOT_FIELDS or attr_name in LocalData.VANILLA_OBJECTS) and \
            isinstance(context.getter_value, list):
            # print "\nCHECKING EQUALITY OF", get_value, "\n\tAGAINST", context.getter_value #, get_value[0] == context.getter_value[0], type(context.getter_value)
            get_value = [get_value] if not isinstance(get_value, list) else get_value
            for each_value in get_value:
                assert_that(context.getter_value, has_items(each_value))
        elif not (isinstance(get_value, (str, unicode)) and get_value.startswith('exists=')):
            assert_that(context.getter_value, equal_to(get_value))
    freezer.stop()


@then(u'I expect that this "(?:.*)" does(?P<_or_not>n\'t)? exists')
def step_impl(context, _or_not):
    if _or_not != 'n\'t':
        assert_that(context.in_db)
    else:
        assert_that(not context.in_db)


@then(u'I do(?P<_or_not>n\'t)? expect to receive "(?P<return_value>.*)" since "(?P<model_type>.*)" does(?:n\'t)? exist')
def step_impl(context, _or_not, return_value, model_type):
    should_exist = _or_not != 'n\'t'
    return_value = None if return_value == "None" else return_value
    if should_exist:
        assert_that(context.in_db, equal_to(getattr(context, 'desired_' + model_type)))
    else:
        assert_that(context.in_db, equal_to(return_value))


# ----- USED IN atom/class.feature ----- #

@then(u'the class "(?:.*)" will exist')
def step_impl(context):
    # we know that if we were able to import it earlier, we're good
    assert_that(context.model)


@then(u'the class "(?:.*)" (?P<required>will require|has optional) (?P<param_or_oneof>parameter|one of) '
      u'"(?P<param_name>.*)" of type "(?P<param_type>.*)"')
def step_impl(context, required, param_or_oneof, param_name, param_type):
    optional_args, required_args = init_args(context.model)
    # TODO: Going to have to figure out how to test that ONE OF the params must be present
    # currently it's a trust thing that we can handle later in an integration test?!?!
    if param_or_oneof == 'one of':
        pass
    else:
        if required == 'will require':
            assert_that(required_args, has_item(param_name))
        else:
            assert_that(optional_args, has_item(param_name))
            # not using the "type" to check --- it's not Java and not strongly typed
            # assert_that(isinstance(getattr(context.model, param_name), eval(param_type)))


# ----- USED TO PRE-LOAD CERTAIN MODELS PRIOR TO TESTING API FUNCTIONALITY ----- #

@given(u'I load "(?P<load_these>\w+)" from (?P<filepath>[\w\/]+)')
def step_impl(context, load_these, filepath):
    loaders = []
    if pluralize(load_these.lower()) == 'clients':
        loaders = ['clients']
    if pluralize(load_these.lower()) == 'groups':
        loaders = ['clients', 'groups']
    if pluralize(load_these.lower()) == 'roles':
        loaders = ['clients', 'groups', 'roles']
    if pluralize(load_these.lower()) == 'users':
        loaders = ['clients', 'groups', 'roles', 'users']

    for loader in loaders:
        context.execute_steps(u'given I load "all" "{model}" from {filepath}'.format(model=loader, filepath=filepath))


@given(u'I load "(?P<num>[\d\w]+)" "(?P<model>\w+)" from (?P<filepath>[\w\/\.]+) belonging to '
       u'"(?P<owner>[^"]+)" "(?P<owner_value>[^"]+)"')
def load_x_models_belonging_to(context, num, model, filepath, owner, owner_value):
    filepath = filepath.replace('/', '.')
    klass = getattr(importlib.import_module(filepath), 'DataLoader')
    modelword = pluralize(model.lower())
    method = getattr(klass, 'create_test_' + modelword)

    extra_args = {owner: make_attr(owner_value)}
    if modelword == 'groups':
        extra_args = make_loadable_args_for_groups(context, extra_args)

    try:
        num = int(num)
        extra_args['num'] = num
    except ValueError:
        pass
    # print "MAKING", modelword, "\nWITH:\t", extra_args
    with LocalData.app.app_context():
        created_things = method(True, **extra_args) if modelword != 'roles' else method(True, **extra_args)
        LocalData.db.session.add_all(created_things.values() if isinstance(created_things, dict) else created_things)
        LocalData.db.session.commit()
        # import pickle
        # print [pickle.loads(e.owner).__dict__ if modelword=='experiments' else e for e in created_things]

    setattr(context, 'loaded_' + modelword, created_things)


@given(u'I load "(?P<num>[\d\w]+)" "(?P<model>\w+)" from (?P<filepath>[\w\/\.]+)(?P<load_others> and load \w+)?'
       u'(?P<with_arg> with extra arg ".*")?')
def load_x_models_from(context, num, model, filepath, load_others=False, with_arg=False):
    filepath = filepath.replace('/', '.')
    klass = getattr(importlib.import_module(filepath), 'DataLoader')
    modelword = pluralize(model.lower())
    method = getattr(klass, 'create_test_' + modelword)

    if with_arg:
        e_arg_key, e_arg_value = with_arg.replace(' with extra arg ', '').replace('"', '').split('=')
    extra_args = {} if not with_arg else {str(e_arg_key): make_attr(e_arg_value)}
    if modelword == 'clients':
        extra_args = make_loadable_args_for_clients(context, filepath, num)
    if modelword == 'groups':
        if load_others:
            context.execute_steps(u'given I load "all" "clients" from {filepath}'.format(filepath=filepath))
        extra_args = make_loadable_args_for_groups(context, extra_args)
    if modelword == 'roles':
        if load_others:
            context.execute_steps(u'given I load "all" "clients" from {filepath}'.format(filepath=filepath))
            context.execute_steps(u'given I load "all" "groups" from {filepath}'.format(filepath=filepath))
        extra_args = make_loadable_args_for_roles(context, filepath)
    if modelword == 'users':
        if load_others:
            context.execute_steps(u'given I load "all" "clients" from {filepath}'.format(filepath=filepath))
            context.execute_steps(u'given I load "all" "groups" from {filepath}'.format(filepath=filepath))
            context.execute_steps(u'given I load "all" "roles" from {filepath}'.format(filepath=filepath))
        extra_args = make_loadable_args_for_users(context, filepath)
    if modelword == 'atoms':
        # if load_others:
        #     context.execute_steps(u'given I load "all" "clients" from {filepath}'.format(filepath=filepath))
        #     context.execute_steps(u'given I load "all" "groups" from {filepath}'.format(filepath=filepath))
        #     context.execute_steps(u'given I load "all" "roles" from {filepath}'.format(filepath=filepath))
        extra_args = make_loadable_args_for_atoms(context)
    if modelword == 'experiments':
        # if load_others:
        #     context.execute_steps(u'given I load "all" "clients" from {filepath}'.format(filepath=filepath))
        #     context.execute_steps(u'given I load "all" "groups" from {filepath}'.format(filepath=filepath))
        #     context.execute_steps(u'given I load "all" "roles" from {filepath}'.format(filepath=filepath))
        extra_args = make_loadable_args_for_experiments(context, extra_args)

    try:
        num = int(num)
        extra_args['num'] = num
    except ValueError:
        pass
    # print "MAKING", modelword, "\nWITH:\t", extra_args
    with LocalData.app.app_context():
        created_things = method(True, **extra_args) if modelword != 'roles' else method(True, **extra_args)
        LocalData.db.session.add_all(created_things.values() if isinstance(created_things, dict) else created_things)
        LocalData.db.session.commit()
        # import pickle
        # print [pickle.loads(e.owner).__dict__ if modelword=='experiments' else e for e in created_things]

    setattr(context, 'loaded_' + modelword, created_things)


@given(u'I want to set "(?P<what_to_set>[\d\w\=\_]+)" "(?P<model>\w+)"\'s "(?P<relation>\w+)"'
       u'(?: using method "(?P<set_method>.*)")? to "(?P<relation_value>.*)"')
def step_impl(context, what_to_set, model, relation, relation_value, set_method=None):
    # set up filtering condition
    if ':' in what_to_set: kw, arg = what_to_set.split(':')
    if '=' in what_to_set: kw, arg = what_to_set.split('=')
    with LocalData.app.app_context():
        chosen_model = load_class('app.models.', model).query.filter_by(**{kw: arg}).one()

        # assume that it's an accessor on the model
        relation_value = make_attr(relation_value, relation, model, context)

        # let's directly set the value(s)
        try:
            if relation in LocalData.MANY_TO_MANY_RELATIONS:
                if isinstance(relation_value, list):
                    setattr(chosen_model, relation, relation_value)
                else:
                    setattr(chosen_model, relation, [relation_value])
            else:
                setattr(chosen_model, relation, relation_value)
        except TypeError, e:
            if str(e).startswith('Incompatible collection type:'):
                setattr(chosen_model, relation, [relation_value])

        # let's set the context.queriable_<model> to chosen_model to use later
        setattr(context, 'queriable_' + model, chosen_model)
        LocalData.db.session.add(chosen_model)
        LocalData.db.session.commit()


@given(u'I want to keep data from the previous scenario')
def step_impl(context): pass


@given(u'I set a (?P<specific_>specific )?"(?P<model>.*)"\'s "(?P<attr_name>.*)" using method '
       u'"(?P<set_method>.*)" to "(?P<attr_value>.*)"')
def step_impl(context, specific_, model, attr_name, set_method, attr_value):
    # we need the actual model we are targetting
    from random import randint
    context.model_name = model
    with LocalData.app.app_context():
        model_class = load_class('app.models.', model)
        if not specific_:  # otherwise we assume we already have context.desired_<model>
            model_count = model_class.query.count()
            setattr(context, 'desired_' + model, model_class.query.get(randint(1, model_count)))
            LocalData.db.session.add(getattr(context, 'desired_' + model))
        setattr(context, model + '_persisted', True)

        if attr_value:  # we want to set a specific value to a field
            # let's make a value properly
            attr_value = make_attr(attr_value, attr_name, model, context)
            model_method(context, set_method, model)(attr_value)
        else:  # want to run some method (that does not require args)
            model_method(context, set_method, model)

        # from app import pp
        # print "CANDIDATE HAS ATTR %s RESET", attr_name
        # pp.pprint(getattr(context, 'desired_' + model).__dict__)
        LocalData.db.session.commit()


# ----- NEW MANNER WITH WICH TO TEST SPECIFIC ATTRIBUTES OF MODELS/CLASSES ----- #

@given(u'I want to set (?P<this_or_that>this|a random) "(?P<model>[\w\.\s]+)"\'s "(?P<attribute>[\w\.\s]+)" to '
       u'"(?P<attr_value>[\w\.:\s\(\)\,\[\]\"\{\}\'\\\]+)"(?: using method ")?(?P<method_to_use>[\w_\.\s]+)?(?:")?')
def step_impl(context, this_or_that, model, attribute, attr_value, method_to_use):
    """
    We want to set up a specific (or random) model with a specific attribute
     *** This will also work with pre-loaded data
    """
    # from app import pp
    # we can reuse a prior step we've defined
    specific_ = 'specific ' if this_or_that.lower() == 'this' else ''
    if method_to_use:
        # this will set context.desired_<model> and call the method <method> (with optional <value>)
        context.execute_steps(u"""
            given I set a {specific}"{model}"'s "{attr}" using method "{method}" to "{value}"
        """.format(specific=specific_, model=model, attr=attribute, method=method_to_use, value=attr_value))
    else:
        # we need the actual model we are targetting
        from random import randint
        context.model_name = model
        with LocalData.app.app_context():
            model_class = load_class('app.models.', model)
            if not specific_:  # otherwise we assume we already have context.desired_<model>
                model_count = model_class.query.count()
                setattr(context, 'desired_' + model, model_class.query.get(randint(1, model_count)))
                # LocalData.db.session.add(getattr(context, 'desired_' + model))
            setattr(context, model + '_persisted', True)

            # let's make a value properly
            attr_value = make_attr(attr_value, attribute, model, context)
            # print "HERE'S WHAT'S IN SESSION:", [obj for obj in LocalData.db.session]
            # print "ABOUT TO SET", attribute, "TO", type(attr_value) , "\n\t", attr_value
            # pp.pprint(getattr(context, 'desired_' + model).__dict__)
            setattr(getattr(context, 'desired_' + model), attribute, attr_value)
            if attribute == 'client_id' and model in ('user', 'user_group'):
                from app.models.clients import Client
                attribute = 'client'
                attr_value = Client.query.get(attr_value)
                # LocalData.db.session.expunge(attr_value)
                # print "THIS CLIENT"
                # pp.pprint(attr_value.__dict__)
                # print "THIS USER"
                if attr_value in LocalData.db.session:
                    # print "MUST GET RID OF", attr_value
                    LocalData.db.session.expunge(attr_value)
                LocalData.db.session.flush()
                # pp.pprint(getattr(context, 'desired_' + model).__dict__)
                setattr(getattr(context, 'desired_' + model), attribute, attr_value)
            # print [obj for obj in LocalData.db.session]
            LocalData.db.session.commit()
            # print "CANDIDATE HAS ATTR %s RESET" % attribute
            # pp.pprint(getattr(context, 'desired_' + model).__dict__)


@given(u'I want a(?:n)? "(?P<model>\w+)" whose "(?P<attr_name>[\w\.]+)"'
       u' (?P<is_or_contains>are not|do not contain) "(?P<attr_value>.*)"')
def step_impl(context, model, is_or_contains, attr_name, attr_value):
    """
    We want to set up a specific (or random) model to use later as context.desired_<model> who has attr = attr_value
     *** This will only work for pre-loaded data
    """
    from random import choice
    candidate = getattr(context, 'desired_' + model) if hasattr(context, 'desired_' + model) else None
    model_klass = load_class('app.models.', model)

    # print load_class('app.models.', model), is_or_contains, attr_name, make_attr(attr_value, context=context)

    if not candidate:
        with LocalData.app.app_context():
            base_query = model_klass.query
            if attr_name in LocalData.MANY_TO_MANY_RELATIONS:
                # all hard-coded for Users / Groups
                from app.models.users import User
                from app.models.usergroups import UserGroup
                filtered = base_query.filter(~User.groups.any(
                    UserGroup.name.is_(make_attr(attr_value, context=context).name)))
            else:
                from sqlalchemy import not_
                filter = {attr_name: make_attr(attr_value, context=context)}
                filtered = base_query.filter_by(not_(**filter))
            candidate = choice(filtered.all())
            setattr(context, 'desired_' + model, candidate)
            # from app import pp
            # pp.pprint(candidate.__dict__)


@given(u'I want a(?:n)?(?: specific)? "(?P<model>\w+)" whose "(?P<attr_name>[\w\.]+)"'
       u' (?P<is_or_contains>is|contains) "(?P<attr_value>.*)"')
def step_impl(context, model, is_or_contains, attr_name, attr_value):
    """
    We want to set up a specific (or random) model to use later as context.desired_<model> who has attr = attr_value
     *** This will only work for pre-loaded data
    """
    from app.models.roles import Role
    from random import choice
    from inflection import singularize
    # from app import pp

    candidate = getattr(context, 'desired_' + model) if hasattr(context, 'desired_' + model) else None
    model_klass = load_class('app.models.', model)
    orig_attr = attr_value
    attr_value = make_attr(attr_value, context=context)

    # print "MADE", attr_value

    def candidate_chooser(basequery, model):
        if model == 'user' and 'superadmin' not in orig_attr:
            return basequery.filter(~model_klass.roles.any(Role.name == 'superadmin')).all()
        else:
            return basequery.all()

    # will have to find one from the db
    if not candidate:
        if attr_name in LocalData.NON_OWNER_RELATIONS:
            klass_to_load = LocalData.relation_to_class[attr_name] if attr_name in LocalData.relation_to_class else attr_name
            attr_klass = load_class('app.models.', singularize(klass_to_load))
            with LocalData.app.app_context():
                rolename = attr_value.name
                candidate_query = model_klass.query.filter(getattr(model_klass, attr_name).
                                                           any(attr_klass.name.is_(rolename)))  # name attr hard-coded

                if not candidate_query.count():
                    candidate_query = model_klass.query
                candidate = choice(candidate_chooser(candidate_query, model))

                client_id = 1 if 'superadmin' not in orig_attr else 1000

                setattr(candidate, attr_name,
                        [attr_klass.query.filter_by(client_id=client_id, name=rolename).one()])  # i.e. user.roles = []
                LocalData.db.session.commit()
                # print "RE-WORKED:"
                # pp.pprint(candidate.__dict__)
        else:
            with LocalData.app.app_context():
                candidate_query = model_klass.query.filter(getattr(model_klass, attr_name) == attr_value)
                # print "\nNON RELATION CANDIDATES: ", candidate_query
                # print "\nNON RELATION CANDIDATES: ", candidate_query.all()
                # print "\nANOTHER WAY", [{"id":c.id, "name":c.name if model != 'user' else c.nickname, attr_name:getattr(c,attr_name)} for c in candidate_query.all()]
                # print "="*100, "\nQUERY", candidate_query, "\n", "="*100
                if not candidate_query.count():
                    candidate_query = model_klass.query.filter(getattr(model_klass, attr_name) == attr_value)
                    # i.e. still none meet our requirements
                    if not candidate_query.count():
                        alter_or_create_model(context, model, model_klass, attr_name, attr_value)
                candidate = choice(candidate_chooser(candidate_query, model))
                # pp.pprint([obj for obj in LocalData.db.session])
                if attr_name in LocalData.RELATIONS_NOT_FIELDS:
                    # print "ATTR NAME", attr_name, "VALUE", attr_value, attr_value in LocalData.db.session
                    # if attr_value in LocalData.db.session:
                    LocalData.db.session.expunge_all()
                # pp.pprint([obj for obj in LocalData.db.session])
                setattr(candidate, attr_name, attr_value)

                LocalData.db.session.commit()
                # print "RE-WORKED:"
                # pp.pprint(candidate.__dict__)
    else:
        if unevaluated_and_namespaced(attr_name):
            attr_name, sub_key = attr_name.split('.', 2)
            if attr_name in LocalData.VANILLA_OBJECTS:
                import pickle
                candidate_value = pickle.loads(getattr(candidate, attr_name))
                setattr(candidate_value, sub_key, attr_value)
                setattr(context, 'candidate_value', candidate_value)
                orig_attr = "eval(pickle.dumps(getattr(context,'candidate_value')))"
        else:
            candidate_value = getattr(candidate, attr_name)
        # check if the other attr is correct...
        if candidate_value != attr_value:
            context.execute_steps(u"""
                Given I want to set "{attrhash}" "{model}"\'s "{attrname}" to "{value}"
            """.format(attrhash='id=' + str(candidate.id), model=model, attrname=attr_name, value=orig_attr))

    # print "\nTHE CANDIDATE IS SET:"
    # pp.pprint(candidate.__dict__)
    setattr(context, 'desired_' + model, candidate)
    setattr(context, model + '_persisted', True)


@given(u'save this "(?P<model>\w+)"\'s "(?P<attr_name>[\w\.]+)" to "(?P<save_location>[\w\.]+)"')
def step_impl(context, model, attr_name, save_location):
    """
    We want to set up a specific (or random) model to use later as context.desired_<model> who has attr = attr_value
     *** This will only work for pre-loaded data
    """
    candidate = getattr(context, 'desired_' + model) if hasattr(context, 'desired_' + model) else None
    if not candidate: assert (False)  # auto-fail

    if unevaluated_and_namespaced(attr_name):
        attr_name, sub_key = attr_name.split('.', 2)
        if attr_name in LocalData.VANILLA_OBJECTS:
            import pickle
            candidate_value = pickle.loads(getattr(candidate, attr_name))
            candidate_value = getattr(candidate_value, sub_key)

    save_to_location(save_location, candidate_value, context)


@given(u'I generate a(?:n)? "(?P<generate_me>[\w\.:\s]+)" using (?P<method_>method )?"(?P<gen_method>[\w\.:\s\(\)]+)"')
def step_impl(context, generate_me, method_, gen_method):
    """
    Special step to generate some value <generate_me> that we want to check at a later time
    """
    # we want to save the generated thing to context.<generate_me>
    if method_:
        generated = model_method(context, gen_method, context.model_name)
    elif is_method(gen_method):
        generated = make_method_from_string(context, gen_method, context.model_name)
    setattr(context, generate_me, generated)


@given(u'I have a "(?P<importable>[\w\.]+)" "(?P<save_import>[\w\.:\s]+)" initialized with '
       u'"(?P<importable_args>[\w\.:\s\[\]\']+)"')
def step_impl(context, importable, save_import, importable_args):
    """
    We aim to import a certain class <importable> and save it to context.<save_import> to be used in a later step
     This may be initialized with <importable_args>
    """
    # import the importable first (which is namespaced and seperated by a '.')
    if is_namespaced(importable):
        mod, klass = importable.split('.')
        importable = load_builtin(mod, klass)
    else:
        importable = load_builtin(importable)

    setattr(context, save_import, importable(eval(importable_args)))


@when(u'I check this "(?P<generated_thing>[\w\.:\s]+)" using "(?P<checker_method>[\w\.:\s\(\)]+)"')
def step_impl(context, generated_thing, checker_method):
    """
    Time to check on what we've created before using the method <checker_method>
    """
    if class_load_reqd(checker_method):
        checker_method = checker_method.split('.')
        klass, method = (checker_method[0], '.'.join(checker_method[1:]))
        # we know that we will have a method
        method_name, margs = method.split('(')
        klass = load_class('app.models.', klass.lower())
        with LocalData.app.app_context():
            if method_has_args(method):
                generated_value = getattr(klass, method_name)(
                    eval(margs[:-1]))  # since we never took care of dangling ')'
            else:
                generated_value = getattr(klass, method_name)()
        setattr(context, 'verified_' + generated_thing, generated_value)
    else:
        with LocalData.app.app_context():
            setattr(context, 'verified_' + generated_thing, eval(checker_method))


@then(u'I should have a "(?P<type_returned>[\w\.:\s]+)" in "(?P<saved_location>[\w]+)" '
      u'containing "(?P<dict_keys>[\w\,\.:\s]+)"')
def step_impl(context, type_returned, saved_location, dict_keys):
    """
    We want to check that the method used previously actually returned:
     a) the type we expected
     (optinally) b) the keys of the dict we expected
    """
    to_check = getattr(context, 'verified_' + saved_location)
    # check type
    assert_that(isinstance(to_check, eval(type_returned)))

    # since it's a dict, check its keys
    for key in [k.strip() for k in dict_keys.split(',')]:
        assert_that(to_check.keys(), has_items(key))


@then(u'the "(?P<saved_location>[\w]+)"\'s "(?P<specific_key>[\w]+)" should match this '
      u'"(?P<model_to_check>[\w]+)"\'s "(?P<attr_to_check>[\w]+)"')
def step_impl(context, saved_location, specific_key, model_to_check, attr_to_check):
    """
    We now want to check the value of each of the keys attributes of the saved thing
    (at context,expected_<saved_location>) against the context.desired_<model_to_check>.<attr_to_check>
    """
    # this works because it's a dict
    to_check = getattr(context, 'verified_' + saved_location)[specific_key]
    assert_that(getattr(getattr(context, 'desired_' + model_to_check), attr_to_check), equal_to(to_check))


@then(u'the return value "(?P<attr>[\w\.]+)" should equal "(?P<what_to_check>[\w\.]+)"')
def step_impl(context, attr, what_to_check):
    """
    We will now check at context.verified_<attr> is the same as context.desired_<what_to_check>
    """
    if is_namespaced(what_to_check):
        what, subwhat = what_to_check.split('.')
        to_check = getattr(getattr(context, 'desired_' + what), subwhat)
    else:
        to_check = getattr(context, 'desired_' + what_to_check)

    if is_namespaced(attr):
        attr, subattr = attr.split('.')
        assert_that(getattr(getattr(context, 'verified_' + attr), subattr), equal_to(to_check))
    else:
        assert_that(getattr(context, 'verified_' + attr), equal_to(to_check))


#     ----- HELPER METHODS -----     #

def save_to_location(location, value, context=None):
    """
    Look for a namespaced location in a dict.

    IF context given:
      Set it to the context.<sublocation>
    ELSE
      Set it to location
    """
    if unevaluated_and_namespaced(location):
        parent_location, sub_location = location.split('.', 2)
        setattr(parent_location if not context else context, sub_location, value)


def alter_or_create_model(context, modelname, klass, attr, value):
    """
    Look for a random type of klass that is possibly persisted and return it.

    Sets context.desired_<modelname>
    """
    from random import choice
    from app.models.users import User
    temp_candidate = klass.query
    if klass == User and attr != 'roles' and value != 'superadmin':
        from app.models.roles import Role
        temp_candidate = temp_candidate.filter(~klass.roles.any(Role.name == 'superadmin'))
    temp_candidate = choice(temp_candidate.all())

    # context.model = klass
    setattr(context, modelname + '_persisted', True)
    context.execute_steps(u"""
        Given I want to set "{attrhash}" "{model}"\'s "{attrname}" to "{value}"
    """.format(attrhash='id=' + str(temp_candidate.id), model=modelname, attrname=attr, value=value))


def produce_comparable(context, get_value):
    """
    Get or create an attribute/relationship based on either its name or a method

    Returns the attribute or method evaluated
    """
    selfdict = klass_useful_args(get_value)
    with LocalData.app.app_context():
        if has_same_attrs(context.getter_value, get_value):
            temp_value, _ = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, type(get_value), **selfdict)
            # merge from DB with get_value winning for missing stuff
            # print "GET VALUE DICT:"
            # from app import pp
            # pp.pprint(selfdict)
            # print "VS..."
            # pp.pprint(temp_value.__dict__)
            for k in get_value.__dict__.keys():
                if k not in temp_value.__dict__:
                    setattr(temp_value, k, getattr(get_value, k))
            get_value = temp_value
        else:
            # print "GET_VALUE DICT:", get_value.__dict__, "\n\tSELF DICT:", selfdict
            get_value, _ = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, type(get_value), **selfdict)
            LocalData.db.session.commit()
    return get_value


def has_same_attrs(persisted_item, incumbent):
    """
    Check on whether or not something that is persisted (in context) has the same attributes as another model.
    """
    itdoes = True
    if isinstance(persisted_item, list):
        for item in persisted_item:
            if set(incumbent.__dict__.keys()) - set(item.__dict__.keys()):
                itdoes = False
    else:
        if set(incumbent.__dict__.keys()) - set(persisted_item.__dict__.keys()):
            itdoes = False
    return itdoes


def make_loadable_args_for_experiments(context, extra_args=None):
    """
    Create the arguments required to call DataLoader.create_test_experiments

    Returns the extra_args dictionary for the method
    """
    if extra_args:
        return extra_args
    if hasattr(context, 'loaded_clients'):
        possible_ids = [v.id for c, v in getattr(context, 'loaded_clients').items() if v.name != 'DeepLearni.ng']
        if len(possible_ids) == 1:
            extra_args = {"client_id": random.choice(possible_ids)}
        else:
            extra_args = {"base_clients": possible_ids}
    else:
        raise (SyntaxError, "CLIENTS must be loaded prior to EXPERIMENTS")
    return extra_args


def make_loadable_args_for_atoms(context):
    """
    Create the arguments required to call DataLoader.create_test_atoms

    Returns the extra_args dictionary for the method
    """
    if hasattr(context, 'loaded_clients'):
        possible_ids = [v.id for c, v in getattr(context, 'loaded_clients').items() if v.name != 'DeepLearni.ng']
        if len(possible_ids) == 1:
            extra_args = {"client_id": random.choice(possible_ids)}
        else:
            extra_args = {"base_clients": possible_ids}
    else:
        raise (SyntaxError, "CLIENTS must be loaded prior to ATOMS")
    return extra_args


def make_loadable_args_for_users(context, filepath):
    """
    Create the arguments required to call DataLoader.create_test_users

    Returns the extra_args dictionary for the method
    """
    roles = getattr(importlib.import_module(filepath), 'base_roles')
    if hasattr(context, 'base_clients'):
        extra_args = {"base_user_roles": roles, "base_clients": getattr(context, 'base_clients')}
    else:
        raise (SyntaxError, "CLIENTS must be loaded prior to USERS")
    return extra_args


def make_loadable_args_for_roles(context, filepath):
    """
    Create the arguments required to call DataLoader.create_test_roles

    Returns the extra_args dictionary for the method
    """
    roles = getattr(importlib.import_module(filepath), 'base_roles')
    if hasattr(context, 'loaded_clients'):
        extra_args = {"base_user_roles": roles, "current_clients": getattr(context, 'loaded_clients')}
    else:
        raise (SyntaxError, "CLIENTS must be loaded prior to ROLES")
    return extra_args


def make_loadable_args_for_groups(context, extra_args=None):
    """
    Create the arguments required to call DataLoader.create_test_groups

    Returns the extra_args dictionary for the method
    """
    if extra_args:
        return extra_args
    if hasattr(context, 'base_clients'):
        extra_args = {"base_clients": getattr(context, 'base_clients')}
    else:
        raise (SyntaxError, "CLIENTS must be loaded prior to GROUPS")
    return extra_args


def make_loadable_args_for_clients(context, filepath, num):
    """
    Create the arguments required to call DataLoader.create_test_clients

    Returns the extra_args dictionary for the method
    """
    import re
    clients = getattr(importlib.import_module(filepath), 'clients') if (not num or num == 'all') else None
    if clients and (isinstance(num, int) or re.match("\d+", num)):
        if int(num) > len(clients):  # we'll have to append some
            while (int(num) > len(clients)): clients.append({"name": faker.company()})
        elif int(num) < len(clients):  # remove some
            clients = clients[:int(num)]
    setattr(context, 'base_clients', clients)
    extra_args = {"base_clients": clients}
    return extra_args


def class_load_reqd(loader):
    """
    Check on whether or not we need to load some class prior to evaluating other expression.

    Returns True if we intend on loading some class
    """
    # We're calling a staticmethod, so it'll be prepended by a class
    if '.' in loader and loader.split('.')[0].istitle():
        return True
    return False


def method_has_args(method):
    """
    Check whether or not an argument of a feature has arguments

    Returns True if the arg of the feature has any arguments itself
    """
    import re
    pattern = re.compile(r'.*\([^\)]+\)')
    return bool(pattern.match(method))


def is_namespaced(importable):
    """
    Check on whether or not some argument is "namespaced" (i.e. has a dot in it)

    Returns True if it does have a '.' in it (i.e. namespaced)
    """
    return '.' in importable


def child_of_method(method):
    """
    Check whether or not an argument from a feature has a possible namespaced arguments itself

    Returns True if the argument contains a possible namespaced method.
    """
    return (method.startswith('eval(') and method.endswith(')') and '.' in method[5:-1])


def is_primative(var_to_check):
    """
    Check whether or not a variable is stricly "primative", defined as int, basestring, bool or FakeDateTime

    Returns True if it is deemed to be primative
    """
    from freezegun.api import FakeDatetime
    return isinstance(var_to_check, (int, basestring, bool, FakeDatetime))


def is_model_attribute(model, attr):
    """
    Check whether or not some attribute is STRICTLY an attribute of the model instance

    Returns True if the attr is STRICLTY an attribute of the model instance.
    """
    return attr in model.__dict__.keys() and not callable(getattr(model, attr))


def load_builtin(module_name, class_name=None):
    """
    Import a specific class or module.
    """
    if class_name:
        return getattr(importlib.import_module(module_name), class_name)
    else:
        return importlib.import_module(module_name)


def vanilla_object(value):
    """
    Check whether or not an instance is STRICTLY a non-db, non-orm type class

    Returns True if the object is STRICTLY a non-orm type class (or if the list's first item is)
    """
    from app.helpers.vanilla_base import VanillaBase
    from app.helpers.db_base import DbBase

    if isinstance(value, list) and value: return vanilla_object(value[0])
    return isinstance(value, VanillaBase) and not isinstance(value, DbBase)


def db_object(value):
    """
    Check whether or not an instance is STRICTLY a db, ORM type class

    Returns True if the object is STRICTLY an ORM type class (or if the list's first item is)
    """
    from app.helpers.db_base import DbBase
    if isinstance(value, list) and value:
        return db_object(value[0])
    return isinstance(value, DbBase)


def klass_useful_args(get_value):
    """
    Find all attributes of the instance of a class that are actual columns, not the relations associated with it

    Return DICT containing only the attributes of this instance
    """
    from sqlalchemy.orm import class_mapper
    important_keys = [p.key for p in class_mapper(type(get_value)).iterate_properties]
    columns_not_relations = [col.name for col in get_value.__table__.columns]
    selfdict = {key: get_value.__dict__[key] for key in get_value.__dict__
                if (key in important_keys and key in columns_not_relations) or
                (key[1:] in important_keys and key[1:] in columns_not_relations)}
    return selfdict


def load_class(base_namespace, model_type):
    """
    Load and import a class from some base namespace.

    Return KLASS that has been imported.
    """
    from inflection import singularize
    try:
        if not (model_type.istitle() or model_type[:1].istitle()):
            klass_name = camelize(model_type.strip('_')) if '_' in model_type else titleize(model_type)
        else:
            klass_name = model_type
        module_name, class_name = str(base_namespace + pluralize(str(klass_name.lower())) + "." + klass_name).rsplit(
            ".", 1)
    except AttributeError:
        module_name, class_name = str(
            base_namespace + pluralize(str(model_type.lower())) + "." + LocalData.word_to_class[model_type]).rsplit(".", 1)

    # print module_name, class_name
    try:
        return getattr(importlib.import_module(module_name, class_name), singularize(class_name))
        # return getattr(importlib.import_module(module_name), class_name)
    except AttributeError:
        return getattr(importlib.import_module(module_name, class_name),
                       singularize(camelize(LocalData.relation_to_class[pluralize(model_type)])))
    except ImportError:
        if '_' in model_type:
            actual_model = LocalData.relation_to_class[model_type.lower()]
            klass_name = camelize(actual_model.strip('_'))
        else:
            klass_name = titleize(model_type)
        module_name, class_name = str(
            base_namespace + pluralize(str(klass_name).lower()) + "." + singularize(klass_name)).rsplit(".", 1)
        # return getattr(importlib.import_module(module_name), class_name)
        return getattr(importlib.import_module(module_name, class_name), singularize(class_name))


def init_args(klass):
    """
    Find the required and optional init arguments for a class

    Return TUPLE containing OPTIONAL arguments AND REQUIRED arguments (with default values)
    """
    orig_args = inspect.getargspec(klass.__init__).args
    orig_defaults = inspect.getargspec(klass.__init__).defaults
    if orig_defaults:
        return orig_args[len(orig_args) - len(orig_defaults):], orig_args[1:len(orig_args) - len(orig_defaults)]
    else:
        return [], orig_args


def is_relations_list(value):
    """
    Check if a list contains makeable class(es)

    Returns True if the value is a list AND appears to require us to make each value
    """
    return isinstance(value, list) and {type(r) for r in value}.issubset({basestring, dict, list, bool})


def load_model_relation(context, relation_name, model_type, attrs=None):
    """
    Load and return a relation attribute of a class (which is itself a model)

    Returns the loaded model itself (from the db if needed)
    """
    # print "THE MODEL RELATION", relation_name, "BELONGING TO", model_type
    class_name = load_class('app.models.',
                            LocalData.relation_to_class[relation_name] if relation_name in LocalData.relation_to_class else relation_name)
    kwargs = getattr(context, model_type + '_attrs')[relation_name] if not attrs else attrs

    _, required_args = init_args(class_name)

    # print "ORIGINALLY HAD", type(getattr(context, model_type + '_attrs')[relation_name]), "PRIMATIVE?", is_primative(getattr(context, model_type + '_attrs')[relation_name])
    if is_primative(kwargs):
        the_relation, _ = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, class_name, kwargs)
    elif isinstance(kwargs, list):
        # print "WE'RE HERE CAUSE IT'S NOT PRIMATIVE, IT'S A LIST", kwargs
        the_relation = load_list_relations(class_name, relation_name, kwargs)
    elif isinstance(kwargs, dict) and all(kws in required_args for kws in kwargs):
        the_relation = load_relation_from_args(context, class_name, kwargs, model_type, relation_name)
    else:
        the_relation = getattr(context, model_type + '_attrs')[relation_name]

    # print "THE RELATION IS", the_relation
    if not attrs:
        setattr(context, 'desired_' + model_type + '_' + relation_name, the_relation)
        setattr(context, 'check_relation', True)
    else:
        return the_relation


def load_relation_from_args(context, class_name, kwargs, model_type, relation_name):
    """
    Load a class relation

    Return the relation itself
    """
    if relation_name in LocalData.VANILLA_OBJECTS:
        the_relation = class_name(**kwargs)
    else:
        the_relation = getattr(context, model_type + '_attrs')[relation_name]
    return the_relation


def load_list_relations(class_name, relation_name, kwargs):
    """
    Load all relations in a list

    Return LIST of loaded relations
    """
    if list(set([isinstance(k, class_name) for k in kwargs])) == [True]:
        return kwargs
    if relation_name in LocalData.VANILLA_OBJECTS:
        the_relation = [class_name(**make_attr(rel)) for rel in kwargs]
    else:
        # print relation_name, type(relation_name), [r for r in kwargs]
        try:
            klass_in_args = load_class('app.models.', singularize(relation_name))
        except ImportError:
            klass_in_args = load_class('app.models.', LocalData.relation_to_class[relation_name])
        # print klass_in_args, {type(r) for r in kwargs}, {type(r) for r in kwargs} == {klass_in_args}
        if {type(r) for r in kwargs} == {klass_in_args}:
            the_relation = kwargs
        else:
            with LocalData.app.app_context():
                the_relation = [LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, class_name, rname)[0] for rname in kwargs]
    return the_relation


def make_attr(value, name=None, model=None, context=None):
    """
    Make attributes based on how they are defined in a feature file (as strings)

    Return INSTANCE of some class based on the params in the string (value)
    """
    # print "ATTEMPTING TO MAKE ATTR FOR:", '\n\tvalue', value, '\n\tname', name, '\n\tmodel', model, '\n\tcontext', context
    if value == 'None':
        return None
    elif isinstance(value, dict):
        return {k: make_attr(v, name=k, context=context) for k, v in value.iteritems()}
    elif isinstance(value, list):
        return [make_attr(item, context=context) for item in value]
    elif isinstance(value, (bool, int, float)):
        return value
    elif isinstance(value, basestring):
        return make_attribute_from_string(context, model, name, value)
    else:
        return value


def make_attribute_from_string(context, model, name, value, replacers={}):
    """
    Tease out the instance we want from a specific string

    Return INSTANCE of some class from a string in a feature file
    """
    # print "NOW MAKING ATTR FROM STRING WITH", model, name, value, "\n\t", replacers

    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    if single_value(value) and [rnd for rnd in ('rand', 'random', 'range') if rnd in value]:
        return make_random_attr(name, value, model)
    elif value.startswith('{'):
        dict_arg, unpacked_args = check_complex_in_dict(value)
        first_pass_dict = recurse_dict_to_make_attrs(dict_arg, unpacked_args) if unpacked_args else dict_arg
        return make_attr(first_pass_dict, context=context)
    elif value.startswith('['):
        if 'context' in value:
            replaceable_list = replace_list_in_string_attr(context, model, name, value, replacers)
            return replacers['LIST_1']
        else:
            list_arg, unpacked_args = check_complex_in_list(value)
            first_pass_list = recurse_list_to_make_attrs(list_arg, unpacked_args, name) if unpacked_args else list_arg
            return make_attr(first_pass_list, context=context)
    elif value.startswith('(') and ').' in value:  # we are requesting some relation that needs to be persisted
        internal_value, external_attr = value.rsplit(').', 1)
        made_value = make_attribute_from_string(context, model, name, internal_value[1:])
        with LocalData.app.app_context():
            LocalData.db.session.add(made_value)
            LocalData.db.session.flush()

        return getattr(made_value, external_attr)
    elif value.startswith('!!!') and value.endswith('!!!'):
        return eval(value[3:-3])
    elif value.startswith('context.'):
        if '.' in value[8:]:
            c, value = value[8:].split('.', 1)
            v = getattr(context, c)
        else:
            return getattr(context, value[8:])

        while '.' in value:
            c, value = value.split('.', 1)
            v = getattr(v, c)
        return getattr(v, value)
    elif value.startswith('eval(') and value.endswith(')'):
        if 'pickle' in value[5:-1]:
            import pickle
        value = value[5:-1]
        if '(' in value and ')' in value:  # assume we are pickle dumping or loading
            loads = 'loads' in value
            # print "CHECKING PICKLED DATA TO EVAL:", value[13:-1], "\n", make_attr(value[13:-1])
            return pickle.loads(make_attr(value[13:-1])) if loads else pickle.dumps(make_attr(value[13:-1]))
        return eval(value)
    elif ':' in value and not (camel_or_title(value) and value.endswith(')')):
        # print ": FOUND"
        return instance_from_string_value(context, value)
    elif 'query' in value:
        model, query = value.split('.', 1)
        query_get_args = query.split('get(', 2)[1][:-1]
        with LocalData.app.app_context():
            return load_class('app.models.', model).query.get(eval(query_get_args))
    elif camel_or_title(value) and value.endswith(')'):
        # print "-"*100, "\nCREATING A CLASS", value
        try:
            import re
            load_klass = re.findall(r"[A-Z][^\)]+\)\)?", value)
            for klass in [tuple(k.replace(')', '', 1).split('(', 1)) for k in load_klass]:
                return create_non_primative(singularize(klass[0].lower()), '')[1](*eval('(' + klass[1] + ')'))
        except SyntaxError:
            pars = prep_fasttype_string_attr(context, model, name, value, replacers)
            # print "\t\t\t\t[PREP FASTTYPE COMPLETE]", pars, "\n\t\t\t\t", pars[-1][-1], "\n", "="*50
        return pars[-1][-1]
    else:
        return value


def prep_fasttype_string_attr(context, model, name, value, replacers={}):
    # print "\n\n........... [FASTTYPE] ENTERING"
    import re
    if '[' in value: value = replace_list_in_string_attr(context, model, name, value, replacers)

    pars = list(parenthetic_contents(value))
    # print "[FASTTYPE] GOT PARS", value, "\n", pars
    for loadable in pars:
        # print "[FASTTYPE] ITERATING PARS", loadable
        loadable_klass = prep_loadable(value, loadable)

        if 'None' in loadable_klass:
            match_close = value.find(')', value.find(loadable[1]) + len(loadable[1]) + 1)
            new_value = value[value.find(loadable[1]) - 1:match_close]
            loadable_klass = new_value[1:][:new_value[1:-1].find('(')].replace('"', '').replace("'", '')
            loadable = [loadable_klass, value[value.find(loadable[1]) - 1:match_close],
                        loadable_klass + value[value.find(loadable[1]) - 1:match_close]]

        loadable_args = []
        special_keys = ['"', "'"]
        while loadable[1].split(',', 1) != [loadable[1]]:
            temp_args = loadable[1].split(',', 1)
            new_temp = temp_args[0]
            loadable[1] = temp_args[1]
            keepgoing = True
            parens = [['parens', 1 if new_temp.count('(') != new_temp.count(')') or
                                      new_temp.count('[') != new_temp.count(']')
            else 0]]
            parens[0][1] += 1 if loadable_klass.startswith('[') else 0
            while keepgoing and 1 in [num[1] for num in [(k, new_temp.count(k) % 2) for k in special_keys] + parens]:
                sub_temp = temp_args[1].split(',', 1)
                temp_args[0] = new_temp + ',' + sub_temp[0]
                new_temp = temp_args[0]
                if len(sub_temp) == 2:
                    temp_args[1] = sub_temp[1]
                    loadable[1] = sub_temp[1]
                else:
                    loadable[1] = ''
                    keepgoing = False
                parens = [('parens', 1 if new_temp.count('(') != new_temp.count(')')
                                          or new_temp.count('[') != new_temp.count(']') else 0)]

            m = re.match(r'^[\'\"](.*)[\'\"]$', temp_args[0].strip())
            if m and m.group(1): temp_args[0] = m.group(1)
            loadable_args.append(temp_args[0].strip())

        # print "\t[FASTTYPE] LOADABLE IS:", loadable
        if loadable[1]:
            loadable_args.append(loadable[1])

        parsed_pars = {p[2]: p[3] for p in pars if len(p) > 3}
        # print "\t[FASTTYPE] LOADABLE ARGS", loadable_args, "\n\t\tPARSED PARS", parsed_pars, "\n\t\tREPLACERS", replacers
        loadable_args = [replacers[l.strip()] if l.strip().startswith('LIST_') else l for l in loadable_args]
        # print "\t[FASTTYPE] REPLACED LOADABLE ARGS", loadable_args, "\n\t\tPARS", pars
        loadable_args = [make_attr(l) if isinstance(l, list) or l not in parsed_pars else parsed_pars[l] for l in
                         loadable_args]

        # print "\t\tREPLACED LOADABLE ARGS", [l[1] for l in [(p[2],p[3]) for p in pars if len(p) > 3] if l[0] in loadable_args]
        # print "\t[FASTTYPE] WANT TO LOAD THIS CLASS", loadable_klass, "\n\t\tARGS:", loadable_args, "\n\t\tLOADABLE:", loadable
        if loadable_klass:
            evaluable_klass = load_class('app.models.', loadable_klass.lower())

            try:
                evaled_class = evaluable_klass(*loadable_args)
            except RuntimeError, e:
                if e.message.startswith('application not registered on db instance'):
                    with LocalData.app.app_context(): evaled_class = evaluable_klass(*loadable_args)
            # print "INITED", evaled_class, "\n\tFOR ARGS:", loadable_args
            if db_object(evaled_class):
                with LocalData.app.app_context():
                    from sqlalchemy import inspect as inspct
                    # from app import pp
                    # print "[FASSTYPE] OBJ IN SESSION?"
                    # pp.pprint(inspct(evaled_class).__dict__)
                    # pp.pprint([obj.__dict__ for obj in LocalData.db.session])
                    if inspct(evaled_class).detached:  # i.e. evaled_class in this session?
                        LocalData.db.session.expunge(evaled_class)
                    evaled_class, created = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, evaluable_klass,
                                                                           **dict(zip(inspect.getargspec(
                                                                               evaluable_klass.__init__).args[1:],
                                                                                      loadable_args)))
                    LocalData.db.session.commit()
        # print "\t\t\t[FASTTYPE] LOADABLE EVAL'ED", evaled_class
        # from app import pp
        # pp.pprint(evaled_class.__dict__)
        # print "\n\t\tLOADABLE[1]", loadable[1], loadable[1].split(',', 1), \
        #     "\n====================================================="
        loadable.append(evaled_class)
        # from app import pp
        # pp.pprint(pars)
    return pars


def prep_loadable(value, loadable):
    import re
    # print "\t\t\tITERATING THROUGH", value
    # print "\t\t\tFINDING", loadable[1]
    # print "\t\t\tWORKING ON", loadable, value[:value.find(loadable[1]) - 1]
    ### REQUIRES SPACES BETWEEN PARAMS WHEN DEFINING "FASSTYPE" INSTANCES (i.e. Atom(param1, param2, ...)
    temp_value = value.replace('None,', '')
    temp_loadable = loadable[1].replace('None,', '')
    loadable_klass = ''.join(
        # reversed(re.findall(r'[^\(\s]*[[A-Z]|(?=\()]', ''.join(reversed(value[:value.find(loadable[1]) - 1])))[0]))
        reversed(
            re.findall(r'[^\(\s]*[[A-Z]|(?=\()]', ''.join(reversed(temp_value[:temp_value.find(temp_loadable) - 1])))[
                0]))
    loadable[0] = loadable_klass
    loadable.append(loadable_klass + '(' + loadable[1] + ')')
    # print "\t\t\tWORKED ON", loadable
    return loadable_klass


def replace_list_in_string_attr(context, model, name, value, replacers):
    import re
    # reverse the opens so that we work our way from the inside out
    opens = list(reversed([m.start() for m in re.finditer('\[', value)]))
    closes = [m.start() for m in re.finditer('\]', value)]
    # print "\tFASTTYPE OPEN BRACKETS", opens, closes

    if len(opens) != len(closes):
        raise ValueError("Please format your string correctly\n%s" % value)
    # ensure we are not recursing into list(s) of list(s)
    for i in range(len(opens)):
        replaceable = value[opens[i]:closes[i] + 1]
        value = value.replace(replaceable, 'LIST_%s' % str(i + 1))

        # print "\tREPLACEABLE", replaceable, "\n\tVALUE NOW", value

        quotable_index_close = -1
        all_quotes = {m.start(): replaceable[m.start()] for m in re.finditer("['|\"]", replaceable)}
        re_list = []

        # print "QUOTES", all_quotes

        # we may have multiple items in each list, let's get them all
        while quotable_index_close < max(all_quotes):
            if quotable_index_close < 0:
                quotable_index = min([m.start() for m in re.finditer("[\"\']", replaceable)])
            else:
                quotable_index = min(
                    [m.start() for m in re.finditer("[\"\']", replaceable[quotable_index_close + 1])]) + \
                                 quotable_index_close + 1
                # min([replaceable[quotable_index_close + 1:].find('"'),
                #                   replaceable[quotable_index_close + 1:].find("'")]) + quotable_index_close + 1

            opening_quote = all_quotes[quotable_index]

            if quotable_index_close < 0:
                quotable_index_close = min(set(
                    [k for k, v in all_quotes.iteritems() if v == opening_quote]) - set([quotable_index]))
            else:
                quotable_index_close = min(set(
                    [k for k, v in all_quotes.iteritems()
                     if k > quotable_index_close and v == opening_quote]) - set([quotable_index]))

            # print "\t\tQUOTABLE INDICES", quotable_index, quotable_index_close, replaceable, "\n\t\t\t", replaceable[quotable_index + 1:quotable_index_close]
            re_list += [
                make_attribute_from_string(context, None, None, replaceable[quotable_index + 1:quotable_index_close],
                                           replacers)]
            # print "\t\tREPLACEABLE LIST", re_list

        # print "REPLACING THE LIST IN REPLACERS", replacers
        replacers['LIST_%s' % str(i + 1)] = re_list
        # print "\t\t[REPLACE LIST IN STRING] REPLACERS:", replacers, "\n\t\t", value

    return value


def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            if not (len(string) > i + 1 and string[i + 1] == '.'):
                yield [len(stack), string[start + 1: i]]


def camel_or_title(s):
    return (s[:1].istitle() and s != s.lower() and s != s.upper())


def single_value(value):
    """
    Check that a value is "makeable" on its own and is not complex in some way

    Return True if this value is "simple" and "single" (i.e. can be made as a random or eval'ed)
    """
    import re
    pattern = re.compile(r'\w+\:\w+|^\w+(\([\w,]+\))?$')
    return bool(pattern.match(value))


def instance_from_string_value(context, value):
    """
    Load a create an instance from a SPECIFICALLY string value

    Return INSTANCE of some class with the params in the string
    """
    value_type, value = value.split(':', 1)  # we will always type these values
    # print "Making Instance FROM STRING:", value_type, value
    # is this value one of our MODELS??  (if titleized <value_type> assume YES)
    if value_type.istitle() or value_type[:1].istitle():
        if pluralize(value_type.lower()) in LocalData.relation_to_class.keys():
            model_name = LocalData.relation_to_class[pluralize(value_type.lower())]
        # print "MAKING A CLASS WITH", model_name, "FOR VALUE:", value
        klass_args, klass_to_make = create_non_primative(model_name, make_attr(value, context=context))

        try:
            inited_klass = klass_to_make(**klass_args)
        except RuntimeError, e:
            if e.message.startswith('application not registered on db instance'):
                with LocalData.app.app_context(): inited_klass = klass_to_make(**klass_args)
        # print "INITED", inited_klass, "\n\tFOR ARGS:", klass_args
        if db_object(inited_klass):
            with LocalData.app.app_context():
                inited_klass, created = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, klass_to_make, **klass_args)
                # print "CREATED?", not created, "THIS", inited_klass
                LocalData.db.session.commit()
                return inited_klass
        else:
            return inited_klass

    if value_type.lower() == 'time':
        import datetime
        value_type = 'datetime.datetime.fromtimestamp'  # obviously from a unix timestamp
        value = float(value)

    # use this for calculating LocalData.UUIDs as well
    value_type = LocalData.UUIDGenerator.int_to_LocalData.UUID if value_type == 'LocalData.UUID' else eval(value_type)

    return value.lower() == 'true' if value_type == bool else value_type(value)


def check_complex_in_list(value):
    """
    Check if the list contains loadable instances

    Returns TUPLE of LIST (evaluated) and LIST (loadable values)
    """
    import ast
    list_arg = ast.literal_eval(value)
    unpacked_args = filter(lambda x: isinstance(x, basestring) and collection_or_loadable(x), list_arg)
    return list_arg, unpacked_args


def check_complex_in_dict(value):
    """
    Check if the list contains loadable instances

    Returns TUPLE of LIST (evaluated) and LIST of TUPLES (loadable values)
    """
    # print "COMPLEX IN DICT", value
    import json
    dict_arg = json.loads(value)
    unpacked_args = [(k, v) for k, v in dict_arg.iteritems() if isinstance(v, basestring) and collection_or_loadable(v)]
    return dict_arg, unpacked_args


def collection_or_loadable(x):
    """
    Check if the value itself is a list or dict OR whether it's loadable as Klass:values

    Returns True if the string is a collection or a loadable class
    """
    return (x[:1] in ('[', '{') or ':' in x)


def recurse_list_to_make_attrs(list_arg, unpacked_args, model=None):
    """
    Recurse through a list and make attributes for each element

    Return LIST of made attributes
    """
    attr_args = [w if w not in unpacked_args else make_attr(w, name=model) for w in list_arg]
    return attr_args


def recurse_dict_to_make_attrs(dict_arg, unpacked_args):
    """
    Recurse through a dictionary and make attributes for each key/value pair

    Return DICT of made attributes
    """
    attr_args = {k: v for k, v in dict_arg.iteritems() if v not in unpacked_args}
    for k, v in unpacked_args:
        attr_args[k] = make_attr(v, k)
    return attr_args


def make_random_attr(attr_name, attr_value, model_type):
    """
    Make a random attribute for a model from a string value

    Return INSTANCE some random instance
    """
    # print "MAKING A RANDOM STRING:", attr_name, attr_value, model_type
    if attr_name:
        try:
            attr_value = getattr(faker, attr_name)()
            return attr_value
        except AttributeError:
            pass

    if ':' in attr_value:
        mytype, attr_value = attr_value.split(':')
    else:
        mytype = None

    if attr_name:
        if attr_name == 'email':
            attr_value = faker.email()
        if attr_name == 'password':
            attr_value = faker.password()
        if str(mytype).lower() == 'int' or attr_name.endswith('id') or attr_name.endswith('type'):
            attr_value = random.randint(1, 1000)
        if attr_name == 'LocalData.UUID' or str(mytype).lower() == 'LocalData.UUID':
            attr_value = LocalData.UUIDGenerator.int_to_LocalData.UUID(random.randint(1, 1000)).hex
        if attr_name == 'nickname':
            attr_value = faker.user_name()
        if attr_name == 'name':
            attr_value = faker.catch_phrase()
            if model_type == 'client':
                attr_value = faker.company()
    if (not mytype or mytype in ('str', 'unicode', 'basestring', 'string')) and isinstance(attr_value,
                                                                                           basestring) and attr_value.startswith(
        'range'):
        lower, upper = attr_value.split(',')
        lower = int(lower[6:])
        upper = int(upper[:-1])
        return random.randint(lower, upper)
    if mytype and str(mytype.lower()) == 'int':
        attr_value = random.randint(1, 1000)

    return attr_value


def private_attr(attr_name):
    """
    Check whether some attribute is intended to be a "private" attribute of a class

    Returns True if the attribute name begins with an underscore
    """
    return attr_name[:1] == '_'


def single_pickled_instance(string):
    return string.startswith('pickle.loads(') and not is_namespaced(string[13:-1])


def unevaluated_and_namespaced(get_method):
    """
    Ensure that a method is not intended to be evaluated AND is namespaced

    Return True if the method does not require "eval" and is namespaced
    """
    return (not get_method.startswith('eval(') and not get_method.startswith('[') and is_namespaced(get_method))


def create_non_primative(attr_name, attr_value, context=None):
    """
    Create an instance of a type of class based on attr_name and its init args attr_value

    Returns INSTANCE of attr_name initialized with attr_value
    """
    model_name = LocalData.relation_to_class[attr_name] if attr_name in LocalData.RELATIONS_NOT_FIELDS or private_attr(
        attr_name) else attr_name
    make_klass = load_class('app.models.', model_name)
    # print "MODEL", model_name, attr_value

    if isinstance(attr_value, make_klass):
        return attr_value, False

    optional_args, required_args = init_args(make_klass)
    klass_args = dict([(el, None) for el in required_args])
    # print "WILL MAKE:", make_klass, "\tWITH REQ:\n\t", required_args, "\tWITH OPT:", optional_args, "\n\tSENDING:", attr_value.keys() if isinstance(attr_value, dict) else attr_value, "OF TYPE:", type(attr_value)
    if not isinstance(attr_value, (list, dict)):
        klass_args['name'] = attr_value
    # elif attr_value.startswith('(') and attr_value.endswith(')'):
    #     klass_args = '(' + attr_value.split('(')[0]
    else:
        if set(set(required_args) - {'self'}).issubset(attr_value.keys()):
            # print "Returning ", type(attr_value), "\n\t", attr_value
            klass_args = attr_value
        elif not LocalData.ModelHelpers.get_one_or_create(LocalData.db.session, make_klass, **attr_value)[1]:
            raise AttributeError(
                "Did not give required arguments %s for class %s" % (required_args, make_klass.__name__))

    # print "RETURNING", make_klass, "WITH\n", klass_args
    return klass_args, make_klass


def is_method(setter):
    """
    Check if the value is actually a method

    Returns True if the string setter appears to be a method
    """
    return setter[-2:] == '()'


def make_method_from_string(context, gargs, model_type):
    """
    Make and return a method from a string

    Returns MIXED the return of a method (from gargs)
    """
    gargs = model_method(context, gargs[:-2], model_type)
    return gargs()


def model_method(context, method_name, model_type):
    """
    Create and return the method (whether global or instance)

    Return INSTANCE of the method_name from model_type
    """
    # print "MODEL METHOD:", context, save_to_location, model_type
    # print "WILL ATTEMPT TO FETCH USING:", context.get_method if 'get_method' in context else context.set_method
    try:
        # We assume that it's part of globals(), but some vars and methods already
        # exist there...  So we check that the actual get_method is a primative type
        getter = globals()[method_name]
        if not is_primative(getter):
            raise KeyError
        else:
            method_name = getter
    except KeyError:
        # below is a relationship in all likelihood
        if hasattr(context, model_type + "_persisted") and getattr(context, model_type + '_persisted'):
            # import pprint
            # print type(getattr(context,'desired_' + model_type))
            # pprint.pprint(getattr(context,'desired_' + model_type).__dict__)
            try:
                from sqlalchemy.orm.exc import DetachedInstanceError
                if hasattr(context, 'desired_' + model_type):
                    prepender = 'desired_'
                else:
                    prepender = 'queriable_'  # hasattr(context, 'queriable_' + model_type)
                from app.schemas.complexschema import is_blobby
                if db_object(getattr(context, prepender + model_type)) and is_blobby(
                    load_class('app.models.', model_type), method_name):
                    with LocalData.app.app_context():
                        model_dict = getattr(context, prepender + model_type).__dict__
                        model_dict.pop('_sa_instance_state')
                        refreshed_model, _ = LocalData.ModelHelpers.get_one_or_create(LocalData.db.session,
                                                                            load_class('app.models.', model_type),
                                                                            **model_dict)
                        setattr(context, prepender + model_type, refreshed_model)
                method_name = getattr(getattr(context, prepender + model_type), method_name)
            except DetachedInstanceError:  # a lazy loaded relation that intends to NOT be loaded
                method_name = getattr(context, 'desired_' + model_type + '_' + method_name)
