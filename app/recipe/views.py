from rest_framework import viewsets, mixins

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient
from recipe.serializers import TagSerializer, IngredientSerializer


class TagViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """return obj for the authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # ဒီဟာက CreateModelMixin ထဲက perform_create method ကို override လုပ်တာ။
    # ဘာလို့လဲ ဆိုတော့ မူရင်း method မှာက user မပါဘူးလေ။ ဘာလို့ဆို ဝင်လာတဲ့
    # payload ထဲမှာ user data မှ မပါတာ။ user data က request.user ကို ယူရမှာ။
    # ဒါကြောင့်မို့ perform_create method ကို override လုပ်တာ။ မဟုတ်ရင်
    # မလိုဘူး။
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
