from django.apps import AppConfig


class IevvJsBaseAppConfig(AppConfig):
    name = 'ievv_opensource.ievv_jsbase'
    verbose_name = "IEVV jsbase"

    def ready(self):
        from django_cradmin import javascriptregistry
        from ievv_opensource.ievv_jsbase import static_components
        javascriptregistry.Registry.get_instance().add(
            static_components.IevvJsBaseCoreComponent)


class IevvJsBaseBasicAppConfig(AppConfig):
    """
    Basic appconfig without any automatic registry updates.
    """
    name = 'ievv_opensource.ievv_jsbase'
    verbose_name = "IEVV jsbase"
