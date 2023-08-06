#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See the file COPYING for details.

from django.conf import settings
from django.test import TestCase

from archaeological_finds.tests import FindInit

from ishtar_common.tests import WizardTest, WizardTestFormData as FormData

from archaeological_warehouse import models, views, forms


class ContainerWizardCreationTest(WizardTest, FindInit, TestCase):
    fixtures = [settings.ROOT_PATH +
                '../fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../ishtar_common/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_files/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_operations/fixtures/initial_data-fr.json',
                settings.ROOT_PATH +
                '../archaeological_finds/fixtures/initial_data-fr.json',
                settings.ROOT_PATH +
                '../archaeological_warehouse/fixtures/initial_data-fr.json',
                ]
    url_name = 'container_creation'
    wizard_name = 'container_wizard'
    steps = views.container_creation_steps
    form_datas = [
        FormData(
            'Container creation',
            form_datas={
                'container-container_creation': {
                    'reference': 'hop-ref',
                    'container_type': None,
                    'location': None,
                    'responsible': None,
                },
                'localisation-container_creation': []
            },
        )
    ]

    def pre_wizard(self):
        main_warehouse = models.Warehouse.objects.create(
            name="Main",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        forms_data = self.form_datas[0].form_datas[
            'container-container_creation']
        forms_data["responsible"] = main_warehouse.pk
        forms_data["location"] = main_warehouse.pk
        forms_data["container_type"] = models.ContainerType.objects.all()[0].pk
        self.container_number = models.Container.objects.count()
        super(ContainerWizardCreationTest, self).pre_wizard()

    def post_wizard(self):
        self.assertEqual(models.Container.objects.count(),
                         self.container_number + 1)


class ContainerTest(FindInit, TestCase):
    fixtures = [settings.ROOT_PATH +
                '../fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../ishtar_common/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_files/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_operations/fixtures/initial_data-fr.json',
                settings.ROOT_PATH +
                '../archaeological_finds/fixtures/initial_data-fr.json',
                settings.ROOT_PATH +
                '../archaeological_warehouse/fixtures/initial_data-fr.json',
                ]

    def testFormCreation(self):
        main_warehouse = models.Warehouse.objects.create(
            name="Main",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        data = {
            'reference': 'hop-ref',
            "responsible": main_warehouse.pk,
            "location": main_warehouse.pk,
            "container_type": models.ContainerType.objects.all()[0].pk
        }
        form = forms.ContainerForm(data=data)
        self.assertTrue(form.is_valid())
        self.container_number = models.Container.objects.count()
        self.create_user()
        form.save(self.user)
        self.assertEqual(models.Container.objects.count(),
                         self.container_number + 1)

    def testChangeLocation(self):
        main_warehouse = models.Warehouse.objects.create(
            name="Main",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        div = models.WarehouseDivision.objects.create(label='division')
        div_link = models.WarehouseDivisionLink.objects.create(
            warehouse=main_warehouse, division=div)

        container = models.Container.objects.create(
            reference="Test", responsible=main_warehouse,
            location=main_warehouse,
            container_type=models.ContainerType.objects.all()[0]
        )
        models.ContainerLocalisation.objects.create(
            container=container, division=div_link,
        )

        self.assertTrue(models.ContainerLocalisation.objects.filter(
            division__warehouse=main_warehouse).count())
        # changing location remove unrelevent localisation
        other_warehouse = models.Warehouse.objects.create(
            name="Other",
            warehouse_type=models.WarehouseType.objects.all()[0]
        )
        container.location = other_warehouse
        container.save()
        self.assertFalse(models.ContainerLocalisation.objects.filter(
            division__warehouse=main_warehouse).count())

