<template lang="html">
    <div class="container" >
        <form :action="application_form_url" method="post" name="new_application" enctype="multipart/form-data">
          <div v-if="!application_readonly">
          <div v-if="hasAmendmentRequest" class="row" style="color:red;">
                <div class="col-lg-12 pull-right">
                  <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title" style="color:red;">An amendment has been requested for this Application
                          <a class="panelClicker" :href="'#'+pBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="pBody">
                                <span class="glyphicon glyphicon-chevron-down pull-right "></span>
                          </a>
                        </h3>
                      </div>
                      <div class="panel-body collapse in" :id="pBody">
                        <div v-for="a in amendment_request">
                          <p>Activity Type:{{a.licence_activity_type.name}}</p>
                          <p>Reason: {{a.reason}}</p>
                          <p>Details: <p v-for="t in splitText(a.text)">{{t}}</p></p>  
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div id="error" v-if="missing_fields.length > 0" style="margin: 10px; padding: 5px; color: red; border:1px solid red;">
                <b>Please answer the following mandatory question(s):</b>
                <ul>
                    <li v-for="error in missing_fields">
                        {{ error.label }}
                    </li>
                </ul>
            </div>

              <Application v-if="application" :application="application">
            
            
                <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
                <input type='hidden' name="schema" :value="JSON.stringify(application)" />
                <input type='hidden' name="application_id" :value="1" />
                <div v-if="!application.readonly" class="row" style="margin-bottom:50px;">
                    <div class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5 ">
                        <div class="navbar-inner">
                            <div class="container">
                                <p class="pull-right" style="margin-top:5px;">
                                    <span v-if="requiresCheckout && wc_version != 1.0"style="margin-right: 5px; font-size: 18px;">
                                        <strong>Estimated application fee: {{application.application_fee | toCurrency}}</strong>
                                        <strong>Estimated licence fee: {{application.licence_fee | toCurrency}}</strong>
                                    </span>
                                    <input type="button" @click.prevent="saveExit" class="btn btn-primary" value="Save and Exit"/>
                                    <input type="button" @click.prevent="save" class="btn btn-primary" value="Save and Continue"/>
                                    <input v-if="!requiresCheckout || wc_version == 1.0" type="button" @click.prevent="submit" class="btn btn-primary" value="Submit"/>
                                    <input v-if="requiresCheckout && wc_version != 1.0" type="button" @click.prevent="submit" class="btn btn-primary" value="Submit and Checkout"/>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else class="row" style="margin-bottom:50px;">
                    <div class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5 ">
                        <div class="navbar-inner">
                            <div class="container">
                                <p class="pull-right" style="margin-top:5px;">
                                    <router-link class="btn btn-primary" :to="{name: 'external-applications-dash'}">Back to Dashboard</router-link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </Application>
        </form>
    </div>
</template>
<script>
import Application from '../form.vue'
import Vue from 'vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
  data: function() {
    return {
      "application": null,
      "loading": [],
      form: null,
      hasAmendmentRequest: false,
      amendment_request: [],
      amendment_request_id:[],
      application_readonly: true,
      pBody: 'pBody',
      application_customer_status_onload: '',
 	  missing_fields: [],
      //current_tab_id: null,
      //current_tab: '',
      //previous_tab: '',
    }
  },
  components: {
    Application
  },
  /*
  watch: {
    // whenever current_tab changes, this function will run
    currentTab: function () {
        // The on tab shown event
        $('.nav-tabs a').on('shown.bs.tab', function (e) {
            alert('Tab has changed');
            //vm.current_tab = e.target;
            //vm.previous_tab = e.relatedTarget;
            vm.current_tab_id = parseInt(e.target.href.split('#')[1]);
        });        
    }
  },
  */
    watch: {
        // whenever current_tab changes, this function will run
        //tabID: function () {
        //current_tab: function () {
        tab_changed: function () {
            let vm = this;
            // The on tab shown event
            $('.nav-tabs a').on('shown.bs.tab', function (e) {
                console.log('Tab has changed: ***' );
                vm.currentTab = $("ul#tabs-section li.active")[0].textContent;
                console.log('Tab has changed: ' + vm.currentTab + ' - ' + vm.tabID);
            });
        }    
    },

  created: function () {
    this.debouncedTabChange = _.debounce(this.get_current_tab, 500)
  },
  computed: {
    isLoading: function() {
      return this.loading.length > 0
    },
    csrf_token: function() {
      return helpers.getCookie('csrftoken')
    },
    application_form_url: function() {
      return (this.application) ? `/api/application/${this.application.id}/draft.json` : '';
    },
    requiresCheckout: function() {
        return this.application.application_fee > 0 && this.application_customer_status_onload == 'Draft'
    },
    wc_version: function (){
        return this.$root.wc_version;
    },
    tab_changed: function() {
      return this.current_tab;
    },
  },
  methods: {
    getSelectedTab: function(obj) {
        alert('Selected Tab Event');
    },
    get_current_tab: function() {
        /*
        vm.previous_tab = vm.current_tab
        vm.current_tab = $("ul#tabs-section li.active")[0].textContent
        return vm.current_tab;
        */
        return $("ul#tabs-section li.active")[0].textContent
    },
    saveExit: function(e) {
      let vm = this;
      let formData = new FormData(vm.form);
      console.log(formData)
      vm.$http.post(vm.application_form_url,formData).then(res=>{
          swal(
            'Saved',
            'Your application has been saved',
            'success'
          ).then((result) => {
            window.location.href = "/";
          });
      },err=>{

      });
    },
    save: function(e) {
      let vm = this;
      let formData = new FormData(vm.form);
      vm.$http.post(vm.application_form_url,formData).then(res=>{
          swal(
            'Saved',
            'Your application has been saved',
            'success'
          )
      },err=>{

      });
    },
    setAmendmentData: function(amendment_request){
      let vm= this;
      vm.amendment_request = amendment_request;
      for(var i=0,_len=vm.amendment_request.length;i<_len;i++){
        vm.amendment_request_id.push(vm.amendment_request[i].licence_activity_type.id)
      }

      if (amendment_request.length > 0){
        vm.hasAmendmentRequest = true;
      }
        
    },
    setdata: function(readonly){
      console.log('from setdata')
      this.application_readonly = readonly;
    },
    splitText: function(aText){
      let newText = '';
      newText = aText.split("\n");
      return newText;
    },


    highlight_missing_fields: function(){
        let vm = this;
        for (var missing_field of vm.missing_fields) {
            $("#" + missing_field.id).css("color", 'red');
        }
    },

    validate: function(){
        let vm = this;
        var required_fields = [];
        var tab_dict = {};

        // reset default colour
        for (var field of vm.missing_fields) {
            $("#" + field.id).css("color", '#515151');
        }
        vm.missing_fields = [];

        /*
        $("#tabs").each(function() {
            $(this).find(".nav-tabs li").each(function(index, element) {
                required_fields.concat(
                    $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden')
                );
            });
        });
        */

        //$("#tabs-section").find("li").each(function(index, element) {
        //$('ul.nav-tabs>li').each(function() {
        /*
        for (var i of $('ul.nav-tabs>li')) {
            // get all required fields, that are not hidden in the DOM
            //var required_fields = $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden');
            i.tab('show')
            required_fields.concat(
                $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden')
            );
        }
        */


        /*
        for (var tab of $('ul.nav-tabs>li>a')) {
            // get all required fields, that are not hidden in the DOM
            tab
                .click()
                .on('shown.bs.tab', function(event){
                    alert('tab shown');
                    var required_fields = $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden');
                    tab_dict[tab.textContent] = required_fields;
                });
        }
        */

        var tab_dict = {};
        for (var tab of $('ul.nav-tabs>li>a')) {
            // get all required fields, that are not hidden in the DOM
            var required_fields = $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required').not(':hidden');
            tab_dict[tab.textContent] = required_fields;
        }

        // loop through all (non-hidden) required fields, and check data has been entered
        //required_fields.each(function() {
        for (var key in tab_dict){
            var required_fields = tab_dict[key];
            required_fields.each(function() {
                //console.log('type: ' + this.type + ' ' + this.name)
                var id = 'id_' + this.name
                if (this.type == 'radio') {
                    //if (this.type == 'radio' && !$("input[name="+this.name+"]").is(':checked')) {
                    if (!$("input[name="+this.name+"]").is(':checked')) {
                        var text = $('#'+id).text()
                        console.log('radio not checked: ' + this.type + ' ' + text)
                        vm.missing_fields.push({id: id, label: text});
                    }
                }

                if (this.type == 'checkbox') {
                    //if (this.type == 'radio' && !$("input[name="+this.name+"]").is(':checked')) {
                    var id = 'id_' + this.classList['value']
                    if ($("[class="+this.classList['value']+"]:checked").length == 0) {
                        var text = $('#'+id).text()
                        console.log('checkbox not checked: ' + this.type + ' ' + text)
                        vm.missing_fields.push({id: id, label: text});
                    }
                }

                if (this.type == 'select-one') {
                    if ($(this).val() == '') {
                        var text = $('#'+id).text()  // this is the (question) label
                        var id = 'id_' + $(this).prop('name'); // the label id
                        console.log('selector not selected: ' + this.type + ' ' + text)
                        vm.missing_fields.push({id: id, label: text});
                    }
                }

                if (this.type == 'file') {
                    var num_files = $('#'+id).attr('num_files')
                    if (num_files == "0") {
                        var text = $('#'+id).text()
                        console.log('file not uploaded: ' + this.type + ' ' + this.name)
                        vm.missing_fields.push({id: id, label: text});
                    }
                }

                if (this.type == 'text') {
                    if (this.value == '') {
                        var text = $('#'+id).text()
                        console.log('text not provided: ' + this.type + ' ' + this.name)
                        vm.missing_fields.push({id: id, label: text});
                    }
                }

                if (this.type == 'textarea') {
                    if (this.value == '') {
                        var text = $('#'+id).text()
                        console.log('textarea not provided: ' + this.type + ' ' + this.name)
                        vm.missing_fields.push({id: id, label: text});
                    }
                }

            });
        }
        return vm.missing_fields.length
    },
    submit: function(){
        let vm = this;
        console.log('SUBMIT VM FORM and CHECKOUT');
        let formData = new FormData(vm.form);

        /*
        var num_missing_fields = vm.validate()
        if (num_missing_fields > 0) {
            vm.highlight_missing_fields()
            var top = ($('#error').offset() || { "top": NaN }).top;
            $('html, body').animate({
                scrollTop: top
            }, 1);
            return false;
        }
        */

        let swal_title = 'Submit Application'
        let swal_html = 'Are you sure you want to submit this application?'
        if (vm.requiresCheckout && vm.wc_version != "1.0") {
            swal_title = 'Submit Application and Checkout'
            swal_html = 'Are you sure you want to submit this application and proceed to checkout?<br><br>' +
                'Upon proceeding, you agree that the system will charge the same credit card used to ' +
                'pay the application fee when your licence is issued.'
        }
        swal({
            title: swal_title,
            html: swal_html,
            type: "question",
            showCancelButton: true,
            confirmButtonText: 'Submit'
        }).then((result) => {
            if (result.value) {
                let formData = new FormData(vm.form);
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.applications,vm.application.id+'/submit'),formData).then(res=>{
                    vm.application = res.body;
                    
                    if (vm.requiresCheckout && vm.wc_version != "1.0") {
                        vm.$http.post(helpers.add_endpoint_join(api_endpoints.applications,vm.application.id+'/application_fee_checkout/'), formData).then(res=>{
                            window.location.href = "/ledger/checkout/checkout/payment-details/";
                        },err=>{
                            swal(
                                'Submit Error',
                                helpers.apiVueResourceError(err),
                                'error'
                            )
                        });
                    } else {
                        vm.$router.push({
                            name: 'submit_application',
                            params: { application: vm.application}
                        });
                    }
                },err=>{
                    swal(
                        'Submit Error',
                        helpers.apiVueResourceError(err),
                        'error'
                    )
                });
            }
        },(error) => {
        });
    },
    fetchAmendmentRequest: function(){
      let vm= this
      console.log("before fetch")
      Vue.http.get(helpers.add_endpoint_json(api_endpoints.applications,vm.application.id+'/amendment_request')).then((res) => {
                // console.log("AMENDMENT REQUEST")
                  console.log("inside fetch amendment request")
                  vm.setAmendmentData(res.body);
              },err=>{
                      
                  });

    },

  },
  
  mounted: function() {
    let vm = this;
    //vm.current_tab = vm.get_current_tab();
    vm.form = document.forms.new_application;

  },

  beforeRouteEnter: function(to, from, next) {
    if (to.params.application_id) {
      let vm= this;
         

         console.log("before fetch application")
      Vue.http.get(`/api/application/${to.params.application_id}.json`).then(res => {
          next(vm => {
            vm.loading.push('fetching application')
            vm.application = res.body;
            vm.loading.splice('fetching application', 1);
            vm.setdata(vm.application.readonly);

            vm.fetchAmendmentRequest();
            vm.application_customer_status_onload = vm.application.customer_status;
          });
        },
        err => {
          console.log(err);
        });
      
    }
    else {
      Vue.http.post('/api/application.json').then(res => {
          next(vm => {
            vm.loading.push('fetching application')
            vm.application = res.body;
            vm.loading.splice('fetching application', 1);
          });
        },
        err => {
          console.log(err);
        });
    }
  }
}
</script>

<style lang="css">
</style>
