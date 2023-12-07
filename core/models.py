from model_utils.models import TimeStampedModel, UUIDModel

nb = dict(null=True, blank=True)


class BaseModel(UUIDModel, TimeStampedModel):
    pass

    class Meta:
        abstract = True
