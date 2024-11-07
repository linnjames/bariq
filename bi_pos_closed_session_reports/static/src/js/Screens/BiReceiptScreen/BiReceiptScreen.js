odoo.define('bi_pos_closed_session_reports.BiReceiptScreen', function (require) {
    'use strict';

    const { Printer } = require('point_of_sale.Printer');
    const { is_email } = require('web.utils');
    const { useRef, useContext } = owl.hooks;
    const { useErrorHandlers, onChangeOrder } = require('point_of_sale.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const AbstractReceiptScreen = require('point_of_sale.AbstractReceiptScreen');
    const { useState } = owl.hooks;

    const BiReceiptScreen = (AbstractReceiptScreen) => {
        class BiReceiptScreen extends AbstractReceiptScreen {
            constructor() {
                super(...arguments);
                this.session_id = this.env.pos.get_order().pos_session_id
                this.biorderReceipt = useRef('order-receipt');
                this.state = useState({main_session_data: [], current_datetime :'', payment_data: '',
                                            state_price_list: '',session_start_time: ''});
            }

            async onSendEmailToCustomer() {
                var session_id = this.env.pos.get_order().pos_session_id
                var input_email = document.getElementById("email").value;
                var mail_format = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                if(input_email.match(mail_format)) {
                    await this.rpc({
                        model: 'pos.session',
                        method: 'send_session_receipt_email',
                        args: ['', input_email, session_id],
                    });
                    document.getElementById('email').value = '';
                } else {
                    alert("You have entered an invalid email address!");
                }
            }

            get currentOrder() {
                return this.env.pos.get_order();
            }

            get nextScreen() {
                return { name: 'ProductScreen' };
            }

            orderDone() {
                this.trigger('close-temp-screen');
                const { name, props } = this.nextScreen;
                this.showScreen(name, props);
            }

            async printReceipt() {
                const currentOrder = this.currentOrder;
                const isPrinted = await this._printReceipt();
                if (isPrinted) {
                    currentOrder._printed = true;
                }
            }

            async my_method2(){
                var self = this;
                var data = await this.rpc({
                    model: 'pos.session',
                    method: 'pos_side_get_session_amount_data',
                    args: [[], this.session_id],
                }).then(async function(output) {
                    if(output){
                        if (self.state.main_session_data.length == 0){
                            self.state.main_session_data.push(output);
                            return self.state.main_session_data
                        }
                    }
                })
            }
            async current_datetime(){
                var self = this;
                var data1 = await this.rpc({
                    model: 'pos.session',
                    method: 'get_real_times',
                    args: [0,self.env.pos.user.tz],
                }).then(async function(output) {
                    if(output){
                        if (self.state.current_datetime == ''){
                            self.state.current_datetime = output;
                            return self.state.current_datetime
                        }
                    }
                })
            }

            async session_start_time(){
                var self = this;
                var data1 = await this.rpc({
                    model: 'pos.session',
                    method: 'get_user_time_zone',
                    args: [0,self.env.pos.pos_session.start_at,self.env.pos.user.tz],
                }).then(async function(output) {
                    if(output){
                        if (self.state.session_start_time == ''){
                            self.state.session_start_time = output;
                            return self.state.session_start_time
                        }
                    }
                })
            }

            async get_payment_data(){
                var self = this;
                var data3 = await this.rpc({
                    model: 'pos.session',
                    method: 'pos_side_get_payment_data',
                    args: [[], this.session_id],
                }).then(async function(output) {
                    if(output){
                        if (self.state.payment_data.length == ''){
                            self.state.payment_data = output;
                            return self.state.payment_data
                        }
                    }
                })
            }

            async get_pricelist(){
                var self = this;
                var data1 = await this.rpc({
                    model: 'pos.session',
                    method: 'pos_side_get_pricelist',
                    args: [[], this.session_id],
                }).then(async function(output) {
                    if(output){
                        if (self.state.state_price_list.length == ''){
                            self.state.state_price_list = output;
                            return self.state.state_price_list
                        }
                    }
                })
            }
        }
        BiReceiptScreen.template = 'BiReceiptScreen';

        return BiReceiptScreen;
    };
    Registries.Component.addByExtending(BiReceiptScreen, AbstractReceiptScreen);

    return BiReceiptScreen;
});
