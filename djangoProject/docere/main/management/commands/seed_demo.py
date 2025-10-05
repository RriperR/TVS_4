# main/management/commands/seed_demo.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Doctor
from django.db import transaction
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Создаёт мок-данные (врачи и их профили). Идемпотентно."

    def add_arguments(self, parser):
        parser.add_argument(
            "--doctors", type=int, default=3,
            help="Сколько создать тестовых врачей (по умолчанию 3)",
        )
        parser.add_argument(
            "--password", type=str, default=None,
            help="Пароль для всех тестовых пользователей (по умолчанию DEMO_PASSWORD или 'demo12345')",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        n = max(0, int(opts["doctors"]))
        password = opts["password"] or os.getenv("DEMO_PASSWORD", "demo12345")

        created = 0
        for i in range(1, n + 1):
            email = f"doc{i}@example.com"
            username = f"doc{i}"
            user, was_created = User.objects.get_or_create(
                email=email,
                defaults=dict(
                    username=username,
                    role="doctor",
                    first_name=f"Доктор{i}",
                    last_name="Тестовый",
                ),
            )
            if was_created:
                user.set_password(password)
                user.save(update_fields=["password"])

            # профиль врача (idемпотентно)
            Doctor.objects.get_or_create(
                user=user,
                defaults=dict(
                    first_name=user.first_name or f"Доктор{i}",
                    last_name=user.last_name or "Тестовый",
                    middle_name=None,
                    specialization="Терапевт",
                    institution="Demo Clinic",
                ),
            )
            created += 1 if was_created else 0

        self.stdout.write(self.style.SUCCESS(
            f"Готово. Всего врачей запрошено: {n}. Новых создано пользователей: {created}."
        ))
