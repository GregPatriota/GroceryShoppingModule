import graphene

from graphene_django import DjangoObjectType, DjangoListField
from .models import Countries


class CountryType(DjangoObjectType):
    class Meta:
        model = Countries
        fields = "__all__"


class Query(graphene.ObjectType):
    all_countries = graphene.List(CountryType)
    country = graphene.Field(CountryType, country_id=graphene.Int())

    def resolve_all_countries(self, info, **kwargs):
        return Countries.objects.all()

    def resolve_country(self, info, country_id):
        return Countries.objects.get(pk=country_id)


class CountryInput(graphene.InputObjectType):
    id = graphene.ID()
    country_name = graphene.String()
    created_at = graphene.DateTime()


class CreateCountry(graphene.Mutation):
    class Arguments:
        country_data = CountryInput(required=True)

    country = graphene.Field(CountryType)

    @staticmethod
    def mutate(root, info, country_data=None):
        country_instance = Countries(
            country_name=country_data.country_name,
            created_at=country_data.created_at
        )
        country_instance.save()
        return CreateCountry(country=country_instance)


class UpdateCountry(graphene.Mutation):
    class Arguments:
        country_data = CountryInput(required=True)

    country = graphene.Field(CountryType)

    @staticmethod
    def mutate(root, info, country_data=None):

        country_instance = Countries.objects.get(pk=country_data.id)

        if country_instance:
            country_instance.country_name = country_data.country_name
            country_instance.created_at = country_data.created_at
            country_instance.save()

            return UpdateCountry(country=country_instance)
        return UpdateCountry(country=None)


class DeleteCountry(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    country = graphene.Field(CountryType)

    @staticmethod
    def mutate(root, info, country_id):
        country_instance = Countries.objects.get(pk=country_id)
        country_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_country = CreateCountry.Field()
    update_country = UpdateCountry.Field()
    delete_country = DeleteCountry.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
