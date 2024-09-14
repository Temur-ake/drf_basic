import graphene
from django.contrib.auth import authenticate
from graphene_django import DjangoObjectType
from graphql_auth.decorators import login_required
import graphql_jwt

from apps.models import Category, ProductHistory, Product, User


class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    balance = graphene.Int()
    type = graphene.String()


class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    price = graphene.Int()
    is_premium = graphene.Boolean()
    description = graphene.String()
    category_id = graphene.ID()
    owner_id = graphene.ID()


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class ProductHistoryType(DjangoObjectType):
    class Meta:
        model = ProductHistory
        fields = '__all__'


# Define GraphQL Mutations

class BulkCreateCategory(graphene.Mutation):
    class Arguments:
        categories = graphene.List(CategoryInput, required=True)

    categories = graphene.List(CategoryType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, categories):
        created_categories = []
        errors = []
        for category_input in categories:
            name = category_input.get('name')
            if Category.objects.filter(name=name).exists():
                errors.append(f"Category '{name}' already exists.")
                continue
            try:
                category = Category.objects.create(name=name)
                created_categories.append(category)
            except Exception as e:
                errors.append(str(e))
        success = len(errors) == 0
        return BulkCreateCategory(
            categories=created_categories,
            success=success,
            message="Categories created successfully." if success else "Errors occurred: " + "; ".join(errors)
        )


class BulkDeleteCategory(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.ID, required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, ids):
        errors = []
        for id in ids:
            try:
                category = Category.objects.get(pk=id)
                category.delete()
            except Category.DoesNotExist:
                errors.append(f"Category with ID {id} not found.")
            except Exception as e:
                errors.append(str(e))
        success = len(errors) == 0
        return BulkDeleteCategory(
            success=success,
            message="Categories deleted successfully." if success else "Errors occurred: " + "; ".join(errors)
        )


class BulkCreateUser(graphene.Mutation):
    class Arguments:
        users = graphene.List(UserInput, required=True)

    users = graphene.List(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, users):
        created_users = []
        errors = []
        for user_input in users:
            try:
                user = User.objects.create_user(
                    username=user_input.get('username'),
                    email=user_input.get('email'),
                    password=user_input.get('password'),
                    balance=user_input.get('balance', 0),
                    type=user_input.get('type', User.Type.USER)
                )
                created_users.append(user)
            except Exception as e:
                errors.append(str(e))
        success = len(errors) == 0
        return BulkCreateUser(
            users=created_users,
            success=success,
            message="Users created successfully." if success else "Errors occurred: " + "; ".join(errors)
        )


class BulkDeleteUser(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.ID, required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, ids):
        errors = []
        for id in ids:
            try:
                user = User.objects.get(pk=id)
                user.delete()
            except User.DoesNotExist:
                errors.append(f"User with ID {id} not found.")
            except Exception as e:
                errors.append(str(e))
        success = len(errors) == 0
        return BulkDeleteUser(
            success=success,
            message="Users deleted successfully." if success else "Errors occurred: " + "; ".join(errors)
        )


class BulkCreateProduct(graphene.Mutation):
    class Arguments:
        products = graphene.List(ProductInput, required=True)

    products = graphene.List(ProductType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, products):
        created_products = []
        errors = []
        for product_input in products:
            try:
                category = Category.objects.get(pk=product_input['category_id'])
                owner = User.objects.get(pk=product_input['owner_id'])
                product = Product.objects.create(
                    name=product_input['name'],
                    price=product_input['price'],
                    is_premium=product_input.get('is_premium', False),
                    description=product_input.get('description'),
                    category=category,
                    owner=owner
                )
                created_products.append(product)
            except Category.DoesNotExist:
                errors.append(f"Category with ID {product_input['category_id']} not found.")
            except User.DoesNotExist:
                errors.append(f"User with ID {product_input['owner_id']} not found.")
            except Exception as e:
                errors.append(str(e))
        success = len(errors) == 0
        return BulkCreateProduct(
            products=created_products,
            success=success,
            message="Products created successfully." if success else "Errors occurred: " + "; ".join(errors)
        )


class BulkDeleteProduct(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.ID, required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, ids):
        errors = []
        for id in ids:
            try:
                product = Product.objects.get(pk=id)
                product.delete()
            except Product.DoesNotExist:
                errors.append(f"Product with ID {id} not found.")
            except Exception as e:
                errors.append(str(e))
        success = len(errors) == 0
        return BulkDeleteProduct(
            success=success,
            message="Products deleted successfully." if success else "Errors occurred: " + "; ".join(errors)
        )


#
# class ObtainJSONWebToken(graphql_jwt.Mutation):
#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#
#     token = graphene.String()
#     refresh_token = graphene.String()
#     payload = graphene.JSONString()
#
#     def mutate(self, info, username, password):
#         user = authenticate(username=username, password=password)
#         if user:
#             token = graphql_jwt.get_token(user)
#             refresh_token = graphql_jwt.get_refresh_token(user)
#             payload = graphql_jwt.decode_jwt_token(token)
#             return ObtainJSONWebToken(
#                 token=token,
#                 refresh_token=refresh_token,
#                 payload=payload
#             )
#         else:
#             raise Exception("Invalid credentials")


class Mutation(graphene.ObjectType):
    bulk_create_category = BulkCreateCategory.Field()
    bulk_delete_category = BulkDeleteCategory.Field()

    bulk_create_user = BulkCreateUser.Field()
    bulk_delete_user = BulkDeleteUser.Field()

    bulk_create_product = BulkCreateProduct.Field()
    bulk_delete_product = BulkDeleteProduct.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    users = graphene.List(UserType)
    products = graphene.List(ProductType, page=graphene.Int(), page_size=graphene.Int(), order_by=graphene.String())

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_products(self, info, page=1, page_size=3, order_by='id', **kwargs):
        qs = Product.objects.order_by(order_by)

        if page and page_size:
            start = (page - 1) * page_size
            end = page * page_size
            qs = qs[start:end]

        return qs


schema = graphene.Schema(query=Query, mutation=Mutation)



