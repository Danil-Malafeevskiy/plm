from django.contrib.auth.models import Group, AnonymousUser, User
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer

from app.models import Feature, Dataset

from app.serializers import FeatureSerializer, DatasetSerializer


class FeatureConsumer(AsyncAPIConsumer):
    groups = list(Group.objects.values_list("name", flat=True))

    @action()
    async def connect(self):
        if self.scope["user"] is not AnonymousUser:
            self.user_id = self.scope["user"].id
            for group in list(self.scope["user"].groups.values_list("name", flat=True)):
                await self.feature_change.subscribe(group=group)
                await self.dataset_change.subscribe(group=group)
            await self.accept()

    @model_observer(Feature)
    async def feature_change(self, message, **kwargs):
        await  self.send_json(message)

    @feature_change.serializer
    def feature_change(self, instance: Feature, action, **kwargs):
        return dict(data=FeatureSerializer(instance).data, action=action.value, pk=instance.pk)

    @feature_change.groups_for_signal
    def feature_change(self, instance: Feature, **kwargs):
        group = Group.objects.get(id=Dataset.objects.get(id=instance.name_id).group_id).name
        yield f'-group__{group}'

    @feature_change.groups_for_consumer
    def feature_change(self, group=None, **kwargs):
        yield f'-group__{group}'

    @model_observer(Dataset)
    async def dataset_change(self, message, **kwargs):
        await  self.send_json(message)

    @dataset_change.serializer
    def dataset_change(self, instance: Feature, action, **kwargs):
        return dict(data=DatasetSerializer(instance).data, action=action.value, pk=instance.pk)

    @dataset_change.groups_for_signal
    def dataset_change(self, instance: Dataset, **kwargs):
        group = Group.objects.get(id=instance.group_id).name
        yield f'-group__{group}'

    @dataset_change.groups_for_consumer
    def dataset_change(self, group=None, **kwargs):
        yield f'-group__{group}'