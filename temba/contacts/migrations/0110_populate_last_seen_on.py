# Generated by Django 2.2.10 on 2020-08-04 15:27

from django.db import migrations, transaction
from django.utils import timezone

BATCH_SIZE = 5000

TYPE_CALL_IN = "mo_call"
TYPE_CALL_IN_MISSED = "mo_miss"
TYPE_NEW_CONVERSATION = "new_conversation"
TYPE_REFERRAL = "referral"
TYPE_STOP_CONTACT = "stop_contact"
SEEN_EVENTS = {TYPE_CALL_IN, TYPE_CALL_IN_MISSED, TYPE_NEW_CONVERSATION, TYPE_REFERRAL, TYPE_STOP_CONTACT}


def calculate_last_seen(apps, org):
    ChannelEvent = apps.get_model("channels", "ChannelEvent")
    Msg = apps.get_model("msgs", "Msg")

    # map of contact id -> last seen date
    last_seen_by_id = {}

    def seen_on(contact_id, date):
        current_last_seen = last_seen_by_id.get(contact_id)
        if not current_last_seen or date > current_last_seen:
            last_seen_by_id[contact_id] = date

    evts = list(
        ChannelEvent.objects.filter(org=org, event_type__in=SEEN_EVENTS).values_list("contact_id", "occurred_on")
    )
    for c_id, occurred_on in evts:
        seen_on(c_id, occurred_on)

    print(f"   - Calculated {len(last_seen_by_id)} last seen values channel events")

    msgs = list(Msg.objects.filter(org=org, direction="I").values_list("contact_id", "created_on"))
    for c_id, created_on in msgs:
        seen_on(c_id, created_on)

    print(f"   - Calculated {len(last_seen_by_id)} last seen values from messages")

    return last_seen_by_id


def populate_last_seen_on_for_org(apps, org):
    Contact = apps.get_model("contacts", "Contact")

    last_seen_by_id = calculate_last_seen(apps, org)

    while last_seen_by_id:
        batch = pop_dict_items(last_seen_by_id, BATCH_SIZE)

        with transaction.atomic():
            for contact_id, last_seen_on in batch:
                Contact.objects.filter(id=contact_id, last_seen_on=None).update(
                    last_seen_on=last_seen_on, modified_on=timezone.now()
                )

        print(f"   - Updated {len(batch)} contacts with new last seen values")


def populate_last_seen_on(apps, schema_editor):
    Org = apps.get_model("orgs", "Org")
    num_orgs = Org.objects.filter(is_active=True).count()

    for o, org in enumerate(Org.objects.filter(is_active=True)):
        populate_last_seen_on_for_org(apps, org)

        print(f" > Updated last_seen_on for org '{org.name}' ({o + 1} / {num_orgs})")


def pop_dict_items(d, count):
    """
    Pop up to count items from the dict d
    """
    items = []
    while len(items) < count:
        try:
            items.append(d.popitem())
        except KeyError:
            break
    return items


def reverse(apps, schema_editor):
    pass


def apply_manual():  # pragma: no cover
    from django.apps import apps

    populate_last_seen_on(apps, None)


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0109_contact_last_seen_on"),
    ]

    operations = [migrations.RunPython(populate_last_seen_on, reverse)]