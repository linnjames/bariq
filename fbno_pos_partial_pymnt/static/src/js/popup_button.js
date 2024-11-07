odoo.define('pos_custom_buttons.PaymentScreenButton', function(require) {
'use strict';
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   const ClientListScreen = require('point_of_sale.ClientDetailsEdit');
    const CustomButtonPaymentScreen = (ClientListScreen) =>

    class extends ClientListScreen {
    constructor() {
    super(...arguments);
    }
    IsCustomButton() {
    // click_invoice
    Gui.showPopup('PayPartialPaymentPopupWidget');
    }
    };
   Registries.Component.extend(ClientListScreen, CustomButtonPaymentScreen);
   return CustomButtonPaymentScreen;
});