odoo.define('custom_pos_keyboard_shortcut.screens', function (require) {
    "use strict";

    const { Gui } = require('point_of_sale.Gui');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const NumpadWidget = require('point_of_sale.NumpadWidget');
    const { posbus } = require('point_of_sale.utils');
    const Registries = require('point_of_sale.Registries');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');

    class ShortcutTipsWidget extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }
        willStart() {
            return super.willStart();
        }
    }
    ShortcutTipsWidget.template = 'ShortcutTipsWidget';
    Registries.Component.add(ShortcutTipsWidget);

    const CustomProductScreen = (ProductScreen) => class extends ProductScreen {
        setup() {
            super.setup();
            this.actionpad = new NumpadWidget(this, {});
            this.actionpad.mount(this.el.querySelector('.placeholder-ActionpadWidget'));
            this.numpad = new NumpadWidget(this, {});
            this.numpad.mount(this.el.querySelector('.placeholder-NumpadWidget'));
            posbus.on('keydown', this, this._onKeydown);
        }

        _onKeydown(ev) {
            const isElementHidden = (selector) => {
                const element = document.querySelector(selector);
                return !element || element.classList.contains('oe_hidden');
            };

            if (!isElementHidden('.product-screen')) {
                if (ev.which === 113) {
                    this.showPopup('ShortcutTipsWidget');
                }
                if (!document.querySelector('.search-input').matches(':focus')) {
                    switch (ev.which) {
                        case 81: this.numpad.state.changeMode('quantity'); break;
                        case 68: this.numpad.state.changeMode('discount'); break;
                        case 80: this.numpad.state.changeMode('price'); break;
                        case 8: this.numpad.state.deleteLastChar(); break;
                        case 109: this.numpad.state.switchSign(); break;
                        case 110: this.numpad.state.appendNewChar('.'); break;
                        case 67: this.showScreen('ClientListScreen'); break;
                        case 32: this.showScreen('PaymentScreen'); break;
                        case 46: this.env.pos.get_order().remove_orderline(this.env.pos.get_order().get_selected_orderline()); break;
                        case 38: this._selectOrderLine('prev'); break;
                        case 40: this._selectOrderLine('next'); break;
                        case 83: {
                            const searchInput = this.el.querySelector('.search-input');
                            if (searchInput) {
                                searchInput.focus();
                                ev.preventDefault();
                            }
                            break;
                        }
                    }
                    if (ev.which >= 96 && ev.which <= 105) {
                        const newChar = String.fromCharCode(ev.which - 48);
                        this.numpad.state.appendNewChar(newChar);
                    }
                }
            }

            // Add handling for other screens as needed
            if (!isElementHidden('.payment-screen').classList.contains('oe_hidden')) {
                if (event.which == 27) {     // click on "Esc" button
                        $($(document).find("div.payment-screen")[0]).find("div.top-content span.back").trigger('click');
                    } else if(event.which == 67) {             // click on "c" button
                        $($(document).find("div.payment-screen")[0]).find("div.js_set_customer").trigger('click');
                    } else if (event.which == 73) {     // click on "i" button
                        $($(document).find("div.payment-screen")[0]).find("div.payment-buttons div.js_invoice").trigger('click');
                    } else if(event.which == 33) {      // click on "Page Up" button
                        if($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight").length > 0){
                            var elem = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight");
                            elem.removeClass("highlight");
                            elem.prev("div.paymentmethod").addClass("highlight");
                        }else{
                            var payMethodLength = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod").length;
                            if(payMethodLength > 0){
                                $($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod")[payMethodLength-1]).addClass('highlight');
                            }
                        }
                    } else if(event.which == 34) {      // click on "Page Down" button
                        if($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight").length > 0){
                            var elem = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight");
                            elem.removeClass("highlight");
                            elem.next("div.paymentmethod").addClass("highlight");
                        }else{
                            var payMethodLength = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod").length;
                            if(payMethodLength > 0){
                                $($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod")[0]).addClass('highlight');
                            }
                        }
                    } else if(event.which == 32) {      // click on "space" button
                        event.preventDefault();
                        $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight").trigger("click");
                        $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod").removeClass("highlight");
                    } else if(event.which == 38) {      // click on "Arrow Up" button
                        if($($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.selected").length > 0){
                            $($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.selected").prev("tr.paymentline").trigger("click");
                        }else{
                            var payLineLength = $($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.paymentline").length;
                            if(payLineLength > 0){
                                $($($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.paymentline")[payLineLength-1]).trigger('click');
                            }
                        }
                    } else if(event.which == 40) {      // click on "Arrow Down" button
                        if($($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.selected").length > 0){
                            var elem = $($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.selected").next("tr.paymentline").trigger("click");
                            elem.removeClass("highlight");
                            elem.next("div.paymentmethod").addClass("highlight");
                        }else{
                            var payLineLength = $($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.paymentline").length;
                            if(payLineLength > 0){
                                $($($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.paymentline")[0]).trigger('click');
                            }
                        }
                    } else if(event.which == 46) {      // click on "Delete" button
                        event.preventDefault();
                        $($(document).find("div.payment-screen")[0]).find("table.paymentlines tbody tr.selected td.delete-button").trigger("click");
                    }
            }

            if (!isElementHidden('.clientlist-screen').classList.contains('oe_hidden')) {
                if (event.which == 27) {            // click on "Esc" button
                        $($(document).find("div.clientlist-screen")[0]).find("span.back").trigger('click');
                    } else if(event.which == 83) {      // click on "s" button
                        $(document).find("div.clientlist-screen span.searchbox input").focus();
                        event.preventDefault();
                    } else if(event.which == 38) {      // click on "Arrow Up" button
                        if($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").length > 0){
                            $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").prev("tr.client-line").click();
                        }else{
                            var clientLineLength = $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line").length;
                            if(clientLineLength > 0){
                                $($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line")[clientLineLength-1]).click();
                            }
                        }
                    } else if(event.which == 40) {      // click on "Arrow Down" button
                        if($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").length > 0){
                            $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").next("tr.client-line").click();
                        }else{
                            var clientLineLength = $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line").length;
                            if(clientLineLength > 0){
                                $($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line")[0]).click();
                            }
                        }
                    } else if(event.which == 13) {      // click on "Enter" button
                        if(!$(document).find("div.clientlist-screen section.top-content span.next").hasClass('oe_hidden')){
                            $(document).find("div.clientlist-screen section.top-content span.next").click();
                        }
                    } else if(event.which == 107) {     // click on numpad "+" button
                        $(document).find("div.clientlist-screen section.top-content span.new-customer").click();
                        $(document).find("div.clientlist-screen section.full-content section.client-details input.client-name").focus();
                        event.preventDefault();
                    }
            }

            if (!isElementHidden('.receipt-screen').classList.contains('oe_hidden')) {
                if(event.which == 73){   // click on "i" button
                        $($(document).find("div.receipt-screen")[0]).find("div.print_invoice").trigger("click");
                    } else if(event.which == 82){   // click on "r" button
                        $($(document).find("div.receipt-screen")[0]).find("div.print").trigger("click");
                    } else if(event.which == 13){   // click on "Enter" button
                        $($(document).find("div.receipt-screen")[0]).find("div.top-content span.next").trigger("click");
                    }
            }

            if (!isElementHidden('.modal-dialog-shortcut-tips').classList.contains('oe_hidden')) {
                if (ev.which === 27) {
                    this.close();
                }
            }
        }

        _selectOrderLine(direction) {
            const selected = this.el.querySelector('ul.orderlines li.selected');
            const target = direction === 'prev' ? selected.previousElementSibling : selected.nextElementSibling;
            if (target) {
                target.click();
            }
        }

        willUnmount() {
            super.willUnmount();
            posbus.off('keydown', this, this._onKeydown);
        }
    };

    Registries.Component.extend(ProductScreen, CustomProductScreen);
});
