webpackJsonp([16],{ULh8:function(t,e){},wqva:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=a("mtWM"),n=a.n(i),s={props:{token:String},data:function(){return{user_data_invitation:{username:"",password:"",first_name:"",last_name:""},user_data:{}}},created:function(){console.log(this.token)},methods:{CreateUser:function(){var t=this;n()({url:"/user-invitations/register/"+this.token+"/",method:"post",data:this.user_data_invitation,headers:{Authorization:"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA4NzY4MTE2LCJqdGkiOiJjMTc1NDBjYmQ0OTA0Yzc3OTEyMjFkNzM1YjhiYzczNyIsInVzZXJfaWQiOjF9.mMMrjOhGFWS-NTTIOpImpcwHR-HMNCQMEmqsp4xrOhY"}}).then(function(e){t.$router.push("/login")}).catch(function(t){alert("error:"+t)})}}},r={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("el-card",{staticClass:"card",staticStyle:{"margin-top":"20px"}},[a("h2",{staticStyle:{"text-align":"center"}},[t._v("\n      创建账户\n    ")]),t._v(" "),a("el-form",{staticClass:"form",staticStyle:{"margin-top":"30px","margin-left":"30%",width:"1000px"},attrs:{"label-width":"140px"}},[a("el-form-item",{staticClass:"form-item-require-lable",attrs:{label:"名(First Name)"}},[a("el-input",{staticStyle:{width:"30%"},model:{value:t.user_data_invitation.first_name,callback:function(e){t.$set(t.user_data_invitation,"first_name",e)},expression:"user_data_invitation.first_name"}})],1),t._v(" "),a("el-form-item",{staticClass:"form-item-require-lable",attrs:{label:"姓(Last Name)"}},[a("el-input",{staticStyle:{width:"30%"},model:{value:t.user_data_invitation.last_name,callback:function(e){t.$set(t.user_data_invitation,"last_name",e)},expression:"user_data_invitation.last_name"}})],1),t._v(" "),a("el-form-item",{staticClass:"form-item-require-lable",attrs:{label:"用户名(Username)"}},[a("el-input",{staticStyle:{width:"30%"},model:{value:t.user_data_invitation.username,callback:function(e){t.$set(t.user_data_invitation,"username",e)},expression:"user_data_invitation.username"}})],1),t._v(" "),a("el-form-item",{staticClass:"form-item-require-lable",attrs:{label:"密码(Password)"}},[a("el-input",{staticStyle:{width:"30%"},attrs:{"show-password":""},model:{value:t.user_data_invitation.password,callback:function(e){t.$set(t.user_data_invitation,"password",e)},expression:"user_data_invitation.password"}})],1),t._v(" "),a("el-form-item",{staticStyle:{"margin-top":"30px","margin-left":"16.2%"}},[a("el-button",{attrs:{type:"primary"},on:{click:t.CreateUser}},[t._v("立即创建")])],1)],1)],1),t._v(" "),a("div")],1)},staticRenderFns:[]};var o={components:{"account-create-invitation":a("VU/8")(s,r,!1,function(t){a("ULh8")},null,null).exports},data:function(){return{token:this.$route.params.token}},created:function(){"true"==this.$store.getters.getUserLoginStatus&&(this.$store.commit("resetState"),location.reload())}},l={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",[e("account-create-invitation",{staticClass:"info",attrs:{token:this.token,height:700}})],1)},staticRenderFns:[]},c=a("VU/8")(o,l,!1,null,null,null);e.default=c.exports}});
//# sourceMappingURL=16.a8cbe3c1614798528181.js.map