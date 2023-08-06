// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.main');
goog.require('cljs.core');
goog.require('reagent.core');
goog.require('org.numenta.sanity.viz_canvas');
goog.require('org.numenta.sanity.helpers');
goog.require('org.numenta.sanity.util');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('org.numenta.sanity.selection');
goog.require('clojure.walk');
goog.require('org.numenta.sanity.controls_ui');
cljs.core.enable_console_print_BANG_();
org.numenta.sanity.main.into_journal = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((65536));
org.numenta.sanity.main.steps = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.PersistentVector.EMPTY);
org.numenta.sanity.main.network_shape = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
org.numenta.sanity.main.selection = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.selection.blank_selection);
org.numenta.sanity.main.capture_options = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
org.numenta.sanity.main.viz_options = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.viz_canvas.default_viz_options);
org.numenta.sanity.main.into_viz = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.main.debug_data = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.controls_ui.default_debug_data);
org.numenta.sanity.main.subscribe_to_steps_BANG_ = (function org$numenta$sanity$main$subscribe_to_steps_BANG_(){
var response_c_68107 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, ["get-capture-options",org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(response_c_68107,true)], null));

var c__38109__auto___68108 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___68108,response_c_68107){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___68108,response_c_68107){
return (function (state_68012){
var state_val_68013 = (state_68012[(1)]);
if((state_val_68013 === (1))){
var state_68012__$1 = state_68012;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68012__$1,(2),response_c_68107);
} else {
if((state_val_68013 === (2))){
var inst_68006 = (state_68012[(2)]);
var inst_68007 = clojure.walk.keywordize_keys(inst_68006);
var inst_68008 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.capture_options,inst_68007) : cljs.core.reset_BANG_.call(null,org.numenta.sanity.main.capture_options,inst_68007));
var inst_68009 = (function (){return ((function (inst_68006,inst_68007,inst_68008,state_val_68013,c__38109__auto___68108,response_c_68107){
return (function (_,___$1,___$2,co){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, ["set-capture-options",clojure.walk.stringify_keys(co)], null));
});
;})(inst_68006,inst_68007,inst_68008,state_val_68013,c__38109__auto___68108,response_c_68107))
})();
var inst_68010 = cljs.core.add_watch(org.numenta.sanity.main.capture_options,cljs.core.cst$kw$org$numenta$sanity$main_SLASH_push_DASH_to_DASH_server,inst_68009);
var state_68012__$1 = (function (){var statearr_68014 = state_68012;
(statearr_68014[(7)] = inst_68008);

return statearr_68014;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_68012__$1,inst_68010);
} else {
return null;
}
}
});})(c__38109__auto___68108,response_c_68107))
;
return ((function (switch__37995__auto__,c__38109__auto___68108,response_c_68107){
return (function() {
var org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_68018 = [null,null,null,null,null,null,null,null];
(statearr_68018[(0)] = org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__);

(statearr_68018[(1)] = (1));

return statearr_68018;
});
var org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____1 = (function (state_68012){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68012);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68019){if((e68019 instanceof Object)){
var ex__37999__auto__ = e68019;
var statearr_68020_68109 = state_68012;
(statearr_68020_68109[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68012);

return cljs.core.cst$kw$recur;
} else {
throw e68019;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68110 = state_68012;
state_68012 = G__68110;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__ = function(state_68012){
switch(arguments.length){
case 0:
return org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____1.call(this,state_68012);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___68108,response_c_68107))
})();
var state__38111__auto__ = (function (){var statearr_68021 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68021[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___68108);

return statearr_68021;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___68108,response_c_68107))
);


var steps_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var response_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, ["get-network-shape",org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(response_c,true)], null));

var c__38109__auto___68111 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___68111,steps_c,response_c){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___68111,steps_c,response_c){
return (function (state_68084){
var state_val_68085 = (state_68084[(1)]);
if((state_val_68085 === (7))){
var state_68084__$1 = state_68084;
var statearr_68086_68112 = state_68084__$1;
(statearr_68086_68112[(2)] = null);

(statearr_68086_68112[(1)] = (8));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68085 === (1))){
var state_68084__$1 = state_68084;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68084__$1,(2),response_c);
} else {
if((state_val_68085 === (4))){
var inst_68082 = (state_68084[(2)]);
var state_68084__$1 = state_68084;
return cljs.core.async.impl.ioc_helpers.return_chan(state_68084__$1,inst_68082);
} else {
if((state_val_68085 === (6))){
var inst_68059 = (state_68084[(7)]);
var inst_68052 = (state_68084[(8)]);
var inst_68055 = clojure.walk.keywordize_keys(inst_68052);
var inst_68056 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.network_shape) : cljs.core.deref.call(null,org.numenta.sanity.main.network_shape));
var inst_68057 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(inst_68055,cljs.core.cst$kw$network_DASH_shape,inst_68056);
var inst_68058 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.capture_options) : cljs.core.deref.call(null,org.numenta.sanity.main.capture_options));
var inst_68059__$1 = cljs.core.cst$kw$keep_DASH_steps.cljs$core$IFn$_invoke$arity$1(inst_68058);
var inst_68060 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps));
var inst_68061 = cljs.core.cons(inst_68057,inst_68060);
var state_68084__$1 = (function (){var statearr_68087 = state_68084;
(statearr_68087[(7)] = inst_68059__$1);

(statearr_68087[(9)] = inst_68061);

return statearr_68087;
})();
if(cljs.core.truth_(inst_68059__$1)){
var statearr_68088_68113 = state_68084__$1;
(statearr_68088_68113[(1)] = (9));

} else {
var statearr_68089_68114 = state_68084__$1;
(statearr_68089_68114[(1)] = (10));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68085 === (3))){
var state_68084__$1 = state_68084;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68084__$1,(5),steps_c);
} else {
if((state_val_68085 === (2))){
var inst_68023 = (state_68084[(2)]);
var inst_68024 = org.numenta.sanity.util.translate_network_shape(inst_68023);
var inst_68025 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.network_shape,inst_68024) : cljs.core.reset_BANG_.call(null,org.numenta.sanity.main.network_shape,inst_68024));
var inst_68026 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_68027 = org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$1(steps_c);
var inst_68028 = ["subscribe",inst_68027];
var inst_68029 = (new cljs.core.PersistentVector(null,2,(5),inst_68026,inst_68028,null));
var inst_68030 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,inst_68029);
var inst_68032 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.network_shape) : cljs.core.deref.call(null,org.numenta.sanity.main.network_shape));
var inst_68033 = cljs.core.cst$kw$regions.cljs$core$IFn$_invoke$arity$1(inst_68032);
var inst_68034 = cljs.core.seq(inst_68033);
var inst_68035 = cljs.core.first(inst_68034);
var inst_68036 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_68035,(0),null);
var inst_68037 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_68035,(1),null);
var inst_68038 = cljs.core.keys(inst_68037);
var inst_68039 = cljs.core.first(inst_68038);
var inst_68040 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_68041 = [cljs.core.cst$kw$dt,cljs.core.cst$kw$path];
var inst_68042 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_68043 = [cljs.core.cst$kw$regions,inst_68036,inst_68039];
var inst_68044 = (new cljs.core.PersistentVector(null,3,(5),inst_68042,inst_68043,null));
var inst_68045 = [(0),inst_68044];
var inst_68046 = cljs.core.PersistentHashMap.fromArrays(inst_68041,inst_68045);
var inst_68047 = [inst_68046];
var inst_68048 = (new cljs.core.PersistentVector(null,1,(5),inst_68040,inst_68047,null));
var inst_68049 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.selection,inst_68048) : cljs.core.reset_BANG_.call(null,org.numenta.sanity.main.selection,inst_68048));
var state_68084__$1 = (function (){var statearr_68090 = state_68084;
(statearr_68090[(10)] = inst_68025);

(statearr_68090[(11)] = inst_68030);

(statearr_68090[(12)] = inst_68049);

return statearr_68090;
})();
var statearr_68091_68115 = state_68084__$1;
(statearr_68091_68115[(2)] = null);

(statearr_68091_68115[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68085 === (11))){
var inst_68069 = (state_68084[(2)]);
var inst_68070 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_68069,(0),null);
var inst_68071 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_68069,(1),null);
var inst_68072 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.steps,inst_68070) : cljs.core.reset_BANG_.call(null,org.numenta.sanity.main.steps,inst_68070));
var inst_68073 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_68074 = [cljs.core.cst$kw$drop_DASH_steps_DASH_data,inst_68071];
var inst_68075 = (new cljs.core.PersistentVector(null,2,(5),inst_68073,inst_68074,null));
var inst_68076 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_viz,inst_68075);
var state_68084__$1 = (function (){var statearr_68092 = state_68084;
(statearr_68092[(13)] = inst_68072);

(statearr_68092[(14)] = inst_68076);

return statearr_68092;
})();
var statearr_68093_68116 = state_68084__$1;
(statearr_68093_68116[(2)] = null);

(statearr_68093_68116[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68085 === (9))){
var inst_68059 = (state_68084[(7)]);
var inst_68061 = (state_68084[(9)]);
var inst_68063 = cljs.core.split_at(inst_68059,inst_68061);
var state_68084__$1 = state_68084;
var statearr_68094_68117 = state_68084__$1;
(statearr_68094_68117[(2)] = inst_68063);

(statearr_68094_68117[(1)] = (11));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68085 === (5))){
var inst_68052 = (state_68084[(8)]);
var inst_68052__$1 = (state_68084[(2)]);
var state_68084__$1 = (function (){var statearr_68095 = state_68084;
(statearr_68095[(8)] = inst_68052__$1);

return statearr_68095;
})();
if(cljs.core.truth_(inst_68052__$1)){
var statearr_68096_68118 = state_68084__$1;
(statearr_68096_68118[(1)] = (6));

} else {
var statearr_68097_68119 = state_68084__$1;
(statearr_68097_68119[(1)] = (7));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68085 === (10))){
var inst_68061 = (state_68084[(9)]);
var inst_68065 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_68066 = [inst_68061,null];
var inst_68067 = (new cljs.core.PersistentVector(null,2,(5),inst_68065,inst_68066,null));
var state_68084__$1 = state_68084;
var statearr_68098_68120 = state_68084__$1;
(statearr_68098_68120[(2)] = inst_68067);

(statearr_68098_68120[(1)] = (11));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68085 === (8))){
var inst_68080 = (state_68084[(2)]);
var state_68084__$1 = state_68084;
var statearr_68099_68121 = state_68084__$1;
(statearr_68099_68121[(2)] = inst_68080);

(statearr_68099_68121[(1)] = (4));


return cljs.core.cst$kw$recur;
} else {
return null;
}
}
}
}
}
}
}
}
}
}
}
});})(c__38109__auto___68111,steps_c,response_c))
;
return ((function (switch__37995__auto__,c__38109__auto___68111,steps_c,response_c){
return (function() {
var org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_68103 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_68103[(0)] = org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__);

(statearr_68103[(1)] = (1));

return statearr_68103;
});
var org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____1 = (function (state_68084){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68084);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68104){if((e68104 instanceof Object)){
var ex__37999__auto__ = e68104;
var statearr_68105_68122 = state_68084;
(statearr_68105_68122[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68084);

return cljs.core.cst$kw$recur;
} else {
throw e68104;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68123 = state_68084;
state_68084 = G__68123;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__ = function(state_68084){
switch(arguments.length){
case 0:
return org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____1.call(this,state_68084);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$main$subscribe_to_steps_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___68111,steps_c,response_c))
})();
var state__38111__auto__ = (function (){var statearr_68106 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68106[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___68111);

return statearr_68106;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___68111,steps_c,response_c))
);


return steps_c;
});
org.numenta.sanity.main.subscription_data = org.numenta.sanity.main.subscribe_to_steps_BANG_();
org.numenta.sanity.main.unsubscribe_BANG_ = (function org$numenta$sanity$main$unsubscribe_BANG_(subscription_data){
var steps_c_68124 = subscription_data;
cljs.core.async.close_BANG_(steps_c_68124);

return cljs.core.remove_watch(org.numenta.sanity.main.viz_options,cljs.core.cst$kw$org$numenta$sanity$main_SLASH_keep_DASH_steps);
});
cljs.core.add_watch(org.numenta.sanity.main.steps,cljs.core.cst$kw$org$numenta$sanity$main_SLASH_recalculate_DASH_selection,(function (_,___$1,___$2,steps){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.selection,(function (p1__68125_SHARP_){
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2((function (sel){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(sel,cljs.core.cst$kw$step,cljs.core.nth.cljs$core$IFn$_invoke$arity$2(steps,cljs.core.cst$kw$dt.cljs$core$IFn$_invoke$arity$1(sel)));
}),p1__68125_SHARP_);
}));
}));
org.numenta.sanity.main.main_pane = (function org$numenta$sanity$main$main_pane(_,___$1){
var size_invalidates_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var c__38109__auto___68191 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___68191,size_invalidates_c){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___68191,size_invalidates_c){
return (function (state_68175){
var state_val_68176 = (state_68175[(1)]);
if((state_val_68176 === (1))){
var state_68175__$1 = state_68175;
var statearr_68177_68192 = state_68175__$1;
(statearr_68177_68192[(2)] = null);

(statearr_68177_68192[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68176 === (2))){
var inst_68160 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_68161 = [cljs.core.cst$kw$drawing,cljs.core.cst$kw$max_DASH_height_DASH_px];
var inst_68162 = (new cljs.core.PersistentVector(null,2,(5),inst_68160,inst_68161,null));
var inst_68163 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.main.viz_options,cljs.core.assoc_in,inst_68162,window.innerHeight);
var state_68175__$1 = (function (){var statearr_68178 = state_68175;
(statearr_68178[(7)] = inst_68163);

return statearr_68178;
})();
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68175__$1,(4),size_invalidates_c);
} else {
if((state_val_68176 === (3))){
var inst_68173 = (state_68175[(2)]);
var state_68175__$1 = state_68175;
return cljs.core.async.impl.ioc_helpers.return_chan(state_68175__$1,inst_68173);
} else {
if((state_val_68176 === (4))){
var inst_68165 = (state_68175[(2)]);
var inst_68166 = (inst_68165 == null);
var state_68175__$1 = state_68175;
if(cljs.core.truth_(inst_68166)){
var statearr_68179_68193 = state_68175__$1;
(statearr_68179_68193[(1)] = (5));

} else {
var statearr_68180_68194 = state_68175__$1;
(statearr_68180_68194[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68176 === (5))){
var state_68175__$1 = state_68175;
var statearr_68181_68195 = state_68175__$1;
(statearr_68181_68195[(2)] = null);

(statearr_68181_68195[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68176 === (6))){
var state_68175__$1 = state_68175;
var statearr_68182_68196 = state_68175__$1;
(statearr_68182_68196[(2)] = null);

(statearr_68182_68196[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68176 === (7))){
var inst_68171 = (state_68175[(2)]);
var state_68175__$1 = state_68175;
var statearr_68183_68197 = state_68175__$1;
(statearr_68183_68197[(2)] = inst_68171);

(statearr_68183_68197[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
return null;
}
}
}
}
}
}
}
});})(c__38109__auto___68191,size_invalidates_c))
;
return ((function (switch__37995__auto__,c__38109__auto___68191,size_invalidates_c){
return (function() {
var org$numenta$sanity$main$main_pane_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$main$main_pane_$_state_machine__37996__auto____0 = (function (){
var statearr_68187 = [null,null,null,null,null,null,null,null];
(statearr_68187[(0)] = org$numenta$sanity$main$main_pane_$_state_machine__37996__auto__);

(statearr_68187[(1)] = (1));

return statearr_68187;
});
var org$numenta$sanity$main$main_pane_$_state_machine__37996__auto____1 = (function (state_68175){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68175);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68188){if((e68188 instanceof Object)){
var ex__37999__auto__ = e68188;
var statearr_68189_68198 = state_68175;
(statearr_68189_68198[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68175);

return cljs.core.cst$kw$recur;
} else {
throw e68188;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68199 = state_68175;
state_68175 = G__68199;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$main$main_pane_$_state_machine__37996__auto__ = function(state_68175){
switch(arguments.length){
case 0:
return org$numenta$sanity$main$main_pane_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$main$main_pane_$_state_machine__37996__auto____1.call(this,state_68175);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$main$main_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$main$main_pane_$_state_machine__37996__auto____0;
org$numenta$sanity$main$main_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$main$main_pane_$_state_machine__37996__auto____1;
return org$numenta$sanity$main$main_pane_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___68191,size_invalidates_c))
})();
var state__38111__auto__ = (function (){var statearr_68190 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68190[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___68191);

return statearr_68190;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___68191,size_invalidates_c))
);


return ((function (size_invalidates_c){
return (function (world_pane,into_sim){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$container_DASH_fluid,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$on_DASH_click,((function (size_invalidates_c){
return (function (){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_viz,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$background_DASH_clicked], null));
});})(size_invalidates_c))
,cljs.core.cst$kw$on_DASH_key_DASH_down,((function (size_invalidates_c){
return (function (p1__68126_SHARP_){
return org.numenta.sanity.viz_canvas.viz_key_down(p1__68126_SHARP_,org.numenta.sanity.main.into_viz);
});})(size_invalidates_c))
,cljs.core.cst$kw$tabIndex,(1)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$row,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.viz_canvas.viz_timeline,org.numenta.sanity.main.steps,org.numenta.sanity.main.selection,org.numenta.sanity.main.capture_options], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$row,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_3$col_DASH_lg_DASH_2,world_pane], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_9$col_DASH_lg_DASH_10,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$overflow,"auto"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.helpers.window_resize_listener,size_invalidates_c], null),new cljs.core.PersistentVector(null, 9, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.viz_canvas.viz_canvas,null,org.numenta.sanity.main.steps,org.numenta.sanity.main.selection,org.numenta.sanity.main.network_shape,org.numenta.sanity.main.viz_options,org.numenta.sanity.main.into_viz,into_sim,org.numenta.sanity.main.into_journal], null)], null)], null)], null);
});
;})(size_invalidates_c))
});
org.numenta.sanity.main.sanity_app = (function org$numenta$sanity$main$sanity_app(title,model_tab,world_pane,current_tab,features,into_sim){
return new cljs.core.PersistentVector(null, 16, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.controls_ui.sanity_app,title,model_tab,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.main_pane,world_pane,into_sim], null),features,org.numenta.sanity.main.capture_options,org.numenta.sanity.main.viz_options,current_tab,org.numenta.sanity.main.selection,org.numenta.sanity.main.steps,org.numenta.sanity.main.network_shape,org.numenta.sanity.viz_canvas.state_colors,org.numenta.sanity.main.into_viz,into_sim,org.numenta.sanity.main.into_journal,org.numenta.sanity.main.debug_data], null);
});
org.numenta.sanity.main.selected_step = (function org$numenta$sanity$main$selected_step(var_args){
var args68200 = [];
var len__7211__auto___68203 = arguments.length;
var i__7212__auto___68204 = (0);
while(true){
if((i__7212__auto___68204 < len__7211__auto___68203)){
args68200.push((arguments[i__7212__auto___68204]));

var G__68205 = (i__7212__auto___68204 + (1));
i__7212__auto___68204 = G__68205;
continue;
} else {
}
break;
}

var G__68202 = args68200.length;
switch (G__68202) {
case 0:
return org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0();

break;
case 2:
return org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args68200.length)].join('')));

}
});

org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0 = (function (){
return org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.steps,org.numenta.sanity.main.selection);
});

org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$2 = (function (steps,selection){
var temp__4657__auto__ = cljs.core.cst$kw$dt.cljs$core$IFn$_invoke$arity$1(cljs.core.first((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selection) : cljs.core.deref.call(null,selection))));
if(cljs.core.truth_(temp__4657__auto__)){
var dt = temp__4657__auto__;
return cljs.core.nth.cljs$core$IFn$_invoke$arity$3((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps) : cljs.core.deref.call(null,steps)),dt,null);
} else {
return null;
}
});

org.numenta.sanity.main.selected_step.cljs$lang$maxFixedArity = 2;
