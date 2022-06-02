from neomodel import (
    RelationshipFrom,
    StringProperty,
    StructuredNode,
)


class Category(StructuredNode):
    name = StringProperty(required=True, unique_index=True)

    podcasts = RelationshipFrom(".podcast.Podcast", "CATEGORIZED_UNDER")
