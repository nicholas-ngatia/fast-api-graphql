from starlette.applications import Starlette
from starlette.routing import Route
from starlette.graphql import GraphQLApp
import graphene
from models import Campaign
from settings import engine
from sqlalchemy.orm import sessionmaker, scoped_session
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField



Session = scoped_session(sessionmaker(bind=engine))


class CreateCampaign(graphene.Mutation):
    id = graphene.Int()
    campaign_name = graphene.String()
    user_email = graphene.String() 


    class Arguments:
        campaign_name = graphene.String()
        user_email = graphene.String()

    def mutate(self, info, user_email, campaign_name):
        session = Session()
        campaign = Campaign(user_email=user_email, campaign_name=campaign_name)
        session.add(campaign)
        session.commit()
        campaign_id = campaign.id
        session.close()

        return CreateCampaign(
            id=campaign_id,
            campaign_name=campaign_name,
            user_email=user_email,
        )

class CampaignContribute(graphene.Mutation):
    id = graphene.Int()
    campaign_name = graphene.String()
    amount_contributed = graphene.Int() 


    class Arguments:
        campaign_id = graphene.Int()
        contribution = graphene.Int()

    def mutate(self, info, campaign_id, contribution):
        session = Session()
        campaign = session.query(Campaign).filter(Campaign.id == campaign_id).first()
        campaign.amount_contributed += contribution
        contributed = campaign.amount_contributed
        campaign_name = campaign.campaign_name
        record_id = campaign.id
        session.add(campaign)
        session.close()

        return CampaignContribute(
            id=record_id,
            campaign_name=campaign_name,
            amount_contributed=contributed,
        )


class Mutation(graphene.ObjectType):
    create_campaign = CreateCampaign.Field()
    campaign_contribute = CampaignContribute.Field()


class CampaignType(SQLAlchemyObjectType):
    class Meta:
        model = Campaign	


class Query(graphene.ObjectType):
    campaign = graphene.List(CampaignType,
    	                     user_email=graphene.String())

    def resolve_campaign(self, info, user_email):
        session = Session()
        print(user_email)
        campaign = session.query(Campaign).filter(Campaign.user_email == user_email).all()
        print(campaign)
        return campaign


routes = [
    Route('/', GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))
]

app = Starlette(routes=routes)