# -*- coding: utf-8 -*-
# @2017, code write by Stella Fredo in Sweden, based on Fleet Management module from Odoo V10.
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    _order = 'id desc'

    def _get_default_state(self):
        state = self.env.ref('fleet.vehicle_state_active', raise_if_not_found=False)
        return state and state.id or False

    license_plate = fields.Char(required=True, help='License plate number of the vehicle (i = plate number for a car)')
    model_id = fields.Many2one('fleet.vehicle.model', 'Model', required=True, help='Model of the vehicle')
    acquisition_date = fields.Date('Built Date', required=False, help='Date when the vehicle has been bought')
    g_color = fields.Selection([('01_Unknown','01 Unknown'), ('02_Blue','02 Blue'),('03_Light_blue','03 Light blue'),('04_Dark_blue','04 Dark blue'),('05_Brown','05 Brown'),('06_Light_brown','06 Light brown'),('07_Dark_Brown','07 Dark Brown'),('08 Grey','08 Grey'),('09_Light_grey','09 Light grey'),('10_Dark_grey','10 Dark grey'),('11_Green','11 Green'),('12_Light_green','12 Light green'),('13_Dark_green','13 Dark green'),('14_Yellow','14 Yellow'),('15_Light_yellow','15 Light yellow'),('16_Red','16 Red'),('17_Light_red','17 Light red'),('18 Dark red','18 Dark red'),('19_Black','19 Black'),('20_White','20 White'),('21 Multi-coloured','21 Multi-coloured'),('22_Purple','22 Purple'),('23_Orange','23 Orange'),('24_Silver','24 Silver')], 'Color', default='01_Unknown', help='Color of the vehicle')
    transmission = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', help='Transmission Used by the vehicle')
    fuel_type = fields.Selection([('G', 'Gasoline'), ('D', 'Diesel'), ('E', 'Electric'), ('H', 'Hybrid')], 'Fuel Type', required=True, default='G', help='Fuel Used by the vehicle')

    @api.depends('model_id', 'license_plate')
    def _compute_vehicle_name(self):
        for record in self:
            record.name = record.license_plate + '/' + record.model_id.name + '/' + record.model_id.brand_id.name

    @api.one
    @api.constrains('vin_sn')
    def _check_unique_constrains(self):
        if (self.vin_sn,'!=','false') and (len(self.search([('vin_sn', 'ilike', self.vin_sn)])) > 1):
             raise ValidationError("VIN already exists and violates unique field constraint")

