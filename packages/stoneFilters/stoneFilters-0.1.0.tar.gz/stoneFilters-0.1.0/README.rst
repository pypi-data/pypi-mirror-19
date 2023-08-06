*************
stonefilters
*************

.. image:: http://gitlab.stonework.net/stoneworksolutions/stonefilters/badges/master/build.svg
     :target: http://gitlab.stonework.net/stoneworksolutions/stonefilters/

.. image:: http://gitlab.stonework.net/stoneworksolutions/stonefilters/badges/master/coverage.svg
     :target: http://gitlab.stonework.net/stoneworksolutions/stonefilters/

Comienzo rapido
---------------

1. Agregar la aplicacion _stoneFilters_ a INSTALLED_APPS::

     INSTALLED_APPS = (
         ...
         "stonefilters",
     )

2. Importar los estaticos:


    <!-- jQuery UI -->
    <script src="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.min.js"></script>
    <link href="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.min.css" rel="stylesheet">
    <link href="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.theme.min.css" rel="stylesheet">
    <link href="{{STATIC_URL}}plugins/jquery-ui-1.12.1/jquery-ui.structure.min.css" rel="stylesheet">


    <!-- MULTISELECT-->
    <link href="{{ STATIC_URL }}css/stoneMultiselect.css" rel="stylesheet"/>
    <script src="{{ STATIC_URL }}js/stoneMultiselect.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}js/stoneFiltersLocalDB.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}lib/jquery-multiselect/src/jquery.multiselect.min.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}lib/jquery-multiselect/src/jquery.multiselect.filter.min.js" type="text/javascript"></script>

    <!-- Add stoneplugins  -->
    <script src="{{STATIC_URL}}js/stoneUtils.js"></script>

    <!-- BLOCKUI -->
    <script src="{{ STATIC_URL }}js/stoneBlock.js" type="text/javascript"></script>


3. Ejemplo de uso:


    stoneselect = new stoneFiltersIU(config, cb)
    stoneselect.createFilters(filters);

