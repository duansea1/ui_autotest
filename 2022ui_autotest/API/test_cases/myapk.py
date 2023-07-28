import apipkg


apipkg.initpkg(__name__, {
    'path': {
        'Class1': "_mypkg.somemodule:Class1",
        'clsattr': "_mypkg.othermodule:Class2.attr",
    }
}
)    