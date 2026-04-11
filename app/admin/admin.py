from models import (Alumoflex, Cable, Color, Construction, Drennage, Marker,
                    Metall, Plastic, Twisting, User)
from sqladmin import ModelView
from sqladmin.filters import (AllUniqueStringValuesFilter, BooleanFilter,
                              ForeignKeyFilter, OperationColumnFilter)


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [User.id, User.first_name, User.second_name, User.email]
    column_details_list = [User.id,
                           User.tg_id,
                           User.email,
                           User.first_name,
                           User.second_name,
                           User.role,
                           User.department,
                           User.is_active,
                           User.is_superuser,
                           User.is_verified]
    column_default_sort = [(User.first_name, True),
                           (User.second_name, True)]
    column_filters = [BooleanFilter(User.is_active),
                      AllUniqueStringValuesFilter(User.department),
                      AllUniqueStringValuesFilter(User.role)]


class CableAdmin(ModelView, model=Cable):
    name = "Кабель"
    name_plural = "Кабеля"
    column_list = [Cable.title, "construction.color.name"]
    column_details_list = [Cable.id,
                           Cable.title,
                           Cable.article,
                           Cable.outer_diametr,
                           Cable.inner_diametr,
                           "construction.name",
                           "drennage.name",
                           "alumoflex.name",
                           "marker.text"]
    form_excluded_columns = ["outer_diametr",
                             "inner_diametr",
                             "title"]
    column_filters = [ForeignKeyFilter(Cable.construction_id,
                                       Construction.name)]


class ConstructionAdmin(ModelView, model=Construction):
    name = "Конструкция"
    name_plural = "Конструкции"
    column_list = [Construction.name, "color.name"]
    column_details_list = [Construction.id,
                           Construction.name,
                           Construction.radial_isolate,
                           Construction.radial_shell,
                           "color.name",
                           "isolate_plastic.name",
                           "shell_plastic.name"]
    form_excluded_columns = ["cable"]
    column_default_sort = [("sort_number", False)]
    column_filters = [OperationColumnFilter(Construction.sort_number)]


class TwistingAdmin(ModelView, model=Twisting):
    name = "Скрученная жила"
    name_plural = "Скрученная жила"
    column_list = ["full_description"]
    column_formatters = {
        "full_description":
        lambda m, a: f"{m.count_wires} x {m.diametr_wires} "
                     f"{m.metall.name if m.metall else '-'}"
                     }
    column_details_list = [Twisting.count_wires,
                           Twisting.diametr_wires,
                           Twisting.diametr_twist,
                           Twisting.resistance,
                           Twisting.step]
    form_excluded_columns = ["cable", "diametr_twist"]
    column_default_sort = [("metall.name", True),
                           (Twisting.count_wires, False),
                           (Twisting.diametr_wires, False)]
    column_filters = [ForeignKeyFilter(Twisting.metall_id, Metall.name)]


class MetallAdmin(ModelView, model=Metall):
    column_list = [Metall.name]
    form_excluded_columns = ["core"]


class AlumoflexAdmin(ModelView, model=Alumoflex):
    column_list = ["title"]
    column_formatters = {
        "title": lambda m, a: f"Alumoflex {m.name}"
    }
    form_excluded_columns = ["cable"]


class DrennageAdmin(ModelView, model=Drennage):
    column_list = [Drennage.name]
    form_excluded_columns = ["cable"]


class PlasticAdmin(ModelView, model=Plastic):
    column_list = [Plastic.name]
    form_excluded_columns = ["shell", "isolate"]


class ColorAdmin(ModelView, model=Color):
    column_list = [Color.name]
    form_excluded_columns = ["constructions"]


class MarkerAdmin(ModelView, model=Marker):
    column_list = [Marker.text]
    form_excluded_columns = ["cable"]
