from recipe.views import RecipesViewSets, TagViewSets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()

router.register("recipes", RecipesViewSets)
router.register("tags", TagViewSets)
app_name = "recipe"
urlpatterns = [path("", include(router.urls))]
