from django.conf import settings
from ledger.accounts.models import EmailUser,OrganisationAddress
from wildlifecompliance.components.organisations.models import (   
                                Organisation,
                                OrganisationContact,
                                OrganisationRequest,
                                OrganisationRequestUserAction,
                                OrganisationAction,
                                OrganisationRequestLogEntry,
                                OrganisationLogEntry,
                                ledger_organisation,
                            )
from wildlifecompliance.components.organisations.utils import (
                                can_manage_org,
                                can_admin_org,
                                is_consultant,
                                can_change_role,
                                can_relink,
                            )
from rest_framework import serializers, status
import rest_framework_gis.serializers as gis_serializers


class LedgerOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ledger_organisation
        fields = '__all__'

class OrganisationCheckSerializer(serializers.Serializer):
    # Validation serializer for new Organisations
    abn = serializers.CharField()
    name = serializers.CharField()

    def validate(self, data):
        requests = OrganisationRequest.objects.filter(abn=data['abn'], role='employee')\
            .exclude(status__in=('declined', 'approved'))
        if requests.exists():
            raise serializers.ValidationError('A request already submitted - Pending Approval.')
        return data

class OrganisationPinCheckSerializer(serializers.Serializer):
    pin1 = serializers.CharField()
    pin2 = serializers.CharField()

class OrganisationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationAddress
        fields = (
            'id',
            'line1',
            'locality',
            'state',
            'country',
            'postcode'
        ) 

class DelegateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name')
    class Meta:
        model = EmailUser
        fields = (
            'id',
            'name',
        )


class OrganisationSerializer(serializers.ModelSerializer):
    address = OrganisationAddressSerializer(read_only=True)
    pins = serializers.SerializerMethodField(read_only=True)
    delegates = DelegateSerializer(many=True, read_only=True)
    organisation = LedgerOrganisationSerializer()

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            'address',
            'email',
            'organisation',
            'phone_number',
            'pins',
            'delegates'
        )

    def get_pins(self, obj):
        try:
            user = self.context['request'].user
            # Check if the request user is among the first five delegates in the organisation
            if can_manage_org(obj, user):
                return {'one': obj.admin_pin_one, 'two': obj.admin_pin_two, 'three': obj.user_pin_one,
                        'four': obj.user_pin_two}
            else:
                return None
        except KeyError:
            return None


class OrganisationCheckExistSerializer(serializers.Serializer):
    # Validation Serializer for existing Organisations
    exists = serializers.BooleanField(default=False)
    id = serializers.IntegerField(default=0)
    first_five = serializers.CharField(allow_blank=True, required=False)
    user = serializers.IntegerField()

    def validate(self, data):
        if data['exists']:
            user = EmailUser.objects.get(id=data['user'])
            org = Organisation.objects.get(id=data['id'])
            if can_relink(org, user):
                raise serializers.ValidationError('Please contact {} to re-link to Organisation'
                                                  .format(data['first_five']))
        return data


class MyOrganisationsSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField(read_only=True)
    is_consultant = serializers.SerializerMethodField(read_only=True)
    can_change_role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            'is_admin',
            'is_consultant',
            'can_change_role'
        )

    def get_is_consultant(self, obj):
        user = self.context['request'].user
        # Check if the request user is among the first five delegates in the organisation
        return is_consultant(obj, user)

    def get_is_admin(self, obj):
        user = self.context['request'].user
        # Check if the request user is among the first five delegates in the organisation
        return can_admin_org(obj, user)

    def get_can_change_role(self, obj):
        user = self.context['request'].user
        # Check if the request user can change their role within the organisation.
        return can_change_role(obj, user)


class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ledger_organisation
        fields = ('id','name')

class OrganisationContactSerializer(serializers.ModelSerializer):
    user_status= serializers.SerializerMethodField()
    user_role= serializers.SerializerMethodField()
    
    class Meta:
        model = OrganisationContact
        fields = '__all__'

    def get_user_status(self,obj):
        return obj.get_user_status_display()

    def get_user_role(self,obj):
        return obj.get_user_role_display()



class OrgRequestRequesterSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = EmailUser
        fields = (
                'email',
                'mobile_number',
                'phone_number',
                'full_name'
                )

    def get_full_name(self, obj):
        return obj.get_full_name()

class OrganisationRequestSerializer(serializers.ModelSerializer):
    identification = serializers.FileField()
    requester = OrgRequestRequesterSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    # role = serializers.SerializerMethodField()
    class Meta:
        model = OrganisationRequest
        fields = '__all__'
        read_only_fields = ('requester','lodgement_date','assigned_officer')

    def get_status(self,obj):
        return obj.get_status_display()
    # def get_role(self,obj):
    #     return obj.get_role_display()


class OrganisationRequestDTSerializer(OrganisationRequestSerializer):
    assigned_officer = serializers.CharField(source='assigned_officer.get_full_name')
    requester = serializers.SerializerMethodField()

    def get_requester(self,obj):
        return obj.requester.get_full_name()

class UserOrganisationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='organisation.name')
    abn = serializers.CharField(source='organisation.abn')
    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn'
        )

class OrganisationRequestActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')
    class Meta:
        model = OrganisationRequestUserAction 
        fields = '__all__'

class OrganisationActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')
    class Meta:
        model = OrganisationAction 
        fields = '__all__'

class OrganisationRequestCommsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationRequestLogEntry
        fields = '__all__'

class OrganisationCommsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationLogEntry
        fields = '__all__'

class OrganisationUnlinkUserSerializer(serializers.Serializer):
    user = serializers.IntegerField()

    def validate(self,obj):
        user = None
        try:
            user = EmailUser.objects.get(id=obj['user'])
            obj['user_obj'] = user
        except EmailUser.DoesNotExist:
            raise serializers.ValidationError('The user you want to unlink does not exist.')
        return obj

class OrgUserAcceptSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name =serializers.CharField()
    email= serializers.EmailField()
    mobile_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, data):
        '''
        Check for either mobile number or phone number
        '''
        if not (data['mobile_number'] or data['phone_number']):
            raise serializers.ValidationError("User must have an associated phone number or mobile number.")
        return data
