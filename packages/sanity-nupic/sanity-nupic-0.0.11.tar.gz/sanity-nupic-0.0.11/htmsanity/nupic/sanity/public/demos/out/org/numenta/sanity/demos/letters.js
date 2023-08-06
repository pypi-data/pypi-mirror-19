// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.letters');
goog.require('cljs.core');
goog.require('goog.dom.forms');
goog.require('goog.dom');
goog.require('reagent.core');
goog.require('org.numenta.sanity.helpers');
goog.require('org.numenta.sanity.main');
goog.require('org.nfrac.comportex.demos.letters');
goog.require('org.numenta.sanity.util');
goog.require('org.numenta.sanity.comportex.data');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('reagent_forms.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.numenta.sanity.bridge.browser');
goog.require('org.numenta.sanity.demos.comportex_common');
goog.require('org.nfrac.comportex.util');
org.numenta.sanity.demos.letters.config = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$n_DASH_regions,(1),cljs.core.cst$kw$world_DASH_buffer_DASH_count,(0)], null));
org.numenta.sanity.demos.letters.world_buffer = cljs.core.async.buffer((5000));
org.numenta.sanity.demos.letters.world_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.letters.world_buffer,cljs.core.comp.cljs$core$IFn$_invoke$arity$2(cljs.core.map.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.util.keep_history_middleware((300),cljs.core.cst$kw$value,cljs.core.cst$kw$history)),cljs.core.map.cljs$core$IFn$_invoke$arity$1((function (p1__71812_SHARP_){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__71812_SHARP_,cljs.core.cst$kw$label,cljs.core.cst$kw$value.cljs$core$IFn$_invoke$arity$1(p1__71812_SHARP_));
}))));
org.numenta.sanity.demos.letters.model = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
org.numenta.sanity.demos.letters.into_sim = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.add_watch(org.numenta.sanity.demos.letters.model,cljs.core.cst$kw$org$numenta$sanity$demos$letters_SLASH_count_DASH_world_DASH_buffer,(function (_,___$1,___$2,___$3){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.letters.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.count(org.numenta.sanity.demos.letters.world_buffer));
}));
org.numenta.sanity.demos.letters.text_to_send = reagent.core.atom.cljs$core$IFn$_invoke$arity$1("Jane has eyes.\nJane has a head.\nJane has a mouth.\nJane has a brain.\nJane has a book.\nJane has no friend.\n\nChifung has eyes.\nChifung has a head.\nChifung has a mouth.\nChifung has a brain.\nChifung has no book.\nChifung has a friend.");
org.numenta.sanity.demos.letters.max_shown = (300);
org.numenta.sanity.demos.letters.scroll_every = (150);
org.numenta.sanity.demos.letters.world_pane = (function org$numenta$sanity$demos$letters$world_pane(){
var show_predictions = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(false);
var selected_htm = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.main.selection,cljs.core.cst$kw$org$numenta$sanity$demos$letters_SLASH_fetch_DASH_selected_DASH_htm,((function (show_predictions,selected_htm){
return (function (_,___$1,___$2,p__71828){
var vec__71829 = p__71828;
var sel1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71829,(0),null);
var temp__4657__auto__ = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(sel1,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$step,cljs.core.cst$kw$snapshot_DASH_id], null));
if(cljs.core.truth_(temp__4657__auto__)){
var snapshot_id = temp__4657__auto__;
var out_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, ["get-model",snapshot_id,org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(out_c,true)], null));

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__71829,sel1,show_predictions,selected_htm){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__71829,sel1,show_predictions,selected_htm){
return (function (state_71834){
var state_val_71835 = (state_71834[(1)]);
if((state_val_71835 === (1))){
var state_71834__$1 = state_71834;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71834__$1,(2),out_c);
} else {
if((state_val_71835 === (2))){
var inst_71831 = (state_71834[(2)]);
var inst_71832 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_htm,inst_71831) : cljs.core.reset_BANG_.call(null,selected_htm,inst_71831));
var state_71834__$1 = state_71834;
return cljs.core.async.impl.ioc_helpers.return_chan(state_71834__$1,inst_71832);
} else {
return null;
}
}
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__71829,sel1,show_predictions,selected_htm))
;
return ((function (switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__71829,sel1,show_predictions,selected_htm){
return (function() {
var org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto____0 = (function (){
var statearr_71839 = [null,null,null,null,null,null,null];
(statearr_71839[(0)] = org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto__);

(statearr_71839[(1)] = (1));

return statearr_71839;
});
var org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto____1 = (function (state_71834){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71834);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71840){if((e71840 instanceof Object)){
var ex__37999__auto__ = e71840;
var statearr_71841_71843 = state_71834;
(statearr_71841_71843[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71834);

return cljs.core.cst$kw$recur;
} else {
throw e71840;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__71844 = state_71834;
state_71834 = G__71844;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto__ = function(state_71834){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto____1.call(this,state_71834);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$letters$world_pane_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__71829,sel1,show_predictions,selected_htm))
})();
var state__38111__auto__ = (function (){var statearr_71842 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71842[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_71842;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__71829,sel1,show_predictions,selected_htm))
);

return c__38109__auto__;
} else {
return null;
}
});})(show_predictions,selected_htm))
);

return ((function (show_predictions,selected_htm){
return (function (){
var temp__4657__auto__ = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_htm) : cljs.core.deref.call(null,selected_htm));
if(cljs.core.truth_(temp__4657__auto__)){
var htm = temp__4657__auto__;
var inval = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(htm);
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$muted,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Input on selected timestep."], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$min_DASH_height,"40vh"], null)], null),org.numenta.sanity.helpers.text_world_input_component(inval,htm,org.numenta.sanity.demos.letters.max_shown,org.numenta.sanity.demos.letters.scroll_every,"")], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$checkbox,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$type,cljs.core.cst$kw$checkbox,cljs.core.cst$kw$checked,(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(show_predictions) : cljs.core.deref.call(null,show_predictions)))?true:null),cljs.core.cst$kw$on_DASH_change,((function (inval,htm,temp__4657__auto__,show_predictions,selected_htm){
return (function (e){
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(show_predictions,cljs.core.not);

return e.preventDefault();
});})(inval,htm,temp__4657__auto__,show_predictions,selected_htm))
], null)], null),"Compute predictions"], null)], null),(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(show_predictions) : cljs.core.deref.call(null,show_predictions)))?org.numenta.sanity.helpers.text_world_predictions_component(htm,(8)):null)], null);
} else {
return null;
}
});
;})(show_predictions,selected_htm))
});
org.numenta.sanity.demos.letters.set_model_BANG_ = (function org$numenta$sanity$demos$letters$set_model_BANG_(){
return org.numenta.sanity.helpers.with_ui_loading_message((function (){
var n_regions = cljs.core.cst$kw$n_DASH_regions.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.letters.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.letters.config)));
var init_QMARK_ = ((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.letters.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.letters.model)) == null);
var G__71849_71853 = org.numenta.sanity.demos.letters.model;
var G__71850_71854 = org.nfrac.comportex.demos.letters.n_region_model.cljs$core$IFn$_invoke$arity$2(n_regions,org.nfrac.comportex.demos.letters.spec);
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__71849_71853,G__71850_71854) : cljs.core.reset_BANG_.call(null,G__71849_71853,G__71850_71854));

if(init_QMARK_){
return org.numenta.sanity.bridge.browser.init.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.letters.model,org.numenta.sanity.demos.letters.world_c,org.numenta.sanity.main.into_journal,org.numenta.sanity.demos.letters.into_sim);
} else {
var G__71851 = org.numenta.sanity.main.network_shape;
var G__71852 = org.numenta.sanity.util.translate_network_shape(org.numenta.sanity.comportex.data.network_shape((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.letters.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.letters.model))));
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__71851,G__71852) : cljs.core.reset_BANG_.call(null,G__71851,G__71852));
}
}));
});
org.numenta.sanity.demos.letters.immediate_key_down_BANG_ = (function org$numenta$sanity$demos$letters$immediate_key_down_BANG_(e){
var temp__4657__auto___71857 = cljs.core.seq(org.nfrac.comportex.demos.letters.clean_text(String.fromCharCode(e.charCode)));
if(temp__4657__auto___71857){
var vec__71856_71858 = temp__4657__auto___71857;
var x_71859 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71856_71858,(0),null);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.letters.world_c,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$value,[cljs.core.str(x_71859)].join('')], null));
} else {
}

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.letters.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.count(org.numenta.sanity.demos.letters.world_buffer));
});
org.numenta.sanity.demos.letters.send_text_BANG_ = (function org$numenta$sanity$demos$letters$send_text_BANG_(){
var temp__4657__auto__ = cljs.core.seq(org.nfrac.comportex.demos.letters.clean_text((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.letters.text_to_send) : cljs.core.deref.call(null,org.numenta.sanity.demos.letters.text_to_send))));
if(temp__4657__auto__){
var xs = temp__4657__auto__;
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,xs,temp__4657__auto__){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,xs,temp__4657__auto__){
return (function (state_71896){
var state_val_71897 = (state_71896[(1)]);
if((state_val_71897 === (1))){
var inst_71888 = (function (){return ((function (state_val_71897,c__38109__auto__,xs,temp__4657__auto__){
return (function org$numenta$sanity$demos$letters$send_text_BANG__$_iter__71884(s__71885){
return (new cljs.core.LazySeq(null,((function (state_val_71897,c__38109__auto__,xs,temp__4657__auto__){
return (function (){
var s__71885__$1 = s__71885;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__71885__$1);
if(temp__4657__auto____$1){
var s__71885__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__71885__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71885__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71887 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71886 = (0);
while(true){
if((i__71886 < size__6924__auto__)){
var x = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71886);
cljs.core.chunk_append(b__71887,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$value,[cljs.core.str(x)].join('')], null));

var G__71908 = (i__71886 + (1));
i__71886 = G__71908;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71887),org$numenta$sanity$demos$letters$send_text_BANG__$_iter__71884(cljs.core.chunk_rest(s__71885__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71887),null);
}
} else {
var x = cljs.core.first(s__71885__$2);
return cljs.core.cons(new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$value,[cljs.core.str(x)].join('')], null),org$numenta$sanity$demos$letters$send_text_BANG__$_iter__71884(cljs.core.rest(s__71885__$2)));
}
} else {
return null;
}
break;
}
});})(state_val_71897,c__38109__auto__,xs,temp__4657__auto__))
,null,null));
});
;})(state_val_71897,c__38109__auto__,xs,temp__4657__auto__))
})();
var inst_71889 = (inst_71888.cljs$core$IFn$_invoke$arity$1 ? inst_71888.cljs$core$IFn$_invoke$arity$1(xs) : inst_71888.call(null,xs));
var inst_71890 = cljs.core.async.onto_chan.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.demos.letters.world_c,inst_71889,false);
var state_71896__$1 = state_71896;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71896__$1,(2),inst_71890);
} else {
if((state_val_71897 === (2))){
var inst_71892 = (state_71896[(2)]);
var inst_71893 = cljs.core.count(org.numenta.sanity.demos.letters.world_buffer);
var inst_71894 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.letters.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,inst_71893);
var state_71896__$1 = (function (){var statearr_71900 = state_71896;
(statearr_71900[(7)] = inst_71892);

return statearr_71900;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_71896__$1,inst_71894);
} else {
return null;
}
}
});})(c__38109__auto__,xs,temp__4657__auto__))
;
return ((function (switch__37995__auto__,c__38109__auto__,xs,temp__4657__auto__){
return (function() {
var org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_71904 = [null,null,null,null,null,null,null,null];
(statearr_71904[(0)] = org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto__);

(statearr_71904[(1)] = (1));

return statearr_71904;
});
var org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto____1 = (function (state_71896){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71896);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71905){if((e71905 instanceof Object)){
var ex__37999__auto__ = e71905;
var statearr_71906_71909 = state_71896;
(statearr_71906_71909[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71896);

return cljs.core.cst$kw$recur;
} else {
throw e71905;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__71910 = state_71896;
state_71896 = G__71910;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto__ = function(state_71896){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto____1.call(this,state_71896);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$letters$send_text_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,xs,temp__4657__auto__))
})();
var state__38111__auto__ = (function (){var statearr_71907 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71907[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_71907;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,xs,temp__4657__auto__))
);

return c__38109__auto__;
} else {
return null;
}
});
org.numenta.sanity.demos.letters.config_template = new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Number of regions:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$n_DASH_regions], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_offset_DASH_5$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.letters.set_model_BANG_();

return e.preventDefault();
})], null),"Restart with new model"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_danger,"This resets all parameters."], null)], null)], null)], null);
org.numenta.sanity.demos.letters.model_tab = (function org$numenta$sanity$demos$letters$model_tab(){
return new cljs.core.PersistentVector(null, 8, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"In this example, text input is presented as a sequence of\n        letters, with independent unique encodings. It is transformed\n        to lower case, and all whitespace is squashed into single\n        spaces."], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"Input ",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Letter sequences"], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_info,[cljs.core.str(cljs.core.cst$kw$world_DASH_buffer_DASH_count.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.letters.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.letters.config)))),cljs.core.str(" queued input values.")].join('')," ",(((cljs.core.cst$kw$world_DASH_buffer_DASH_count.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.letters.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.letters.config))) > (0)))?new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_warning$btn_DASH_xs,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
var c__38109__auto___71999 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___71999){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___71999){
return (function (state_71974){
var state_val_71975 = (state_71974[(1)]);
if((state_val_71975 === (7))){
var inst_71960 = (state_71974[(2)]);
var state_71974__$1 = state_71974;
var statearr_71976_72000 = state_71974__$1;
(statearr_71976_72000[(2)] = inst_71960);

(statearr_71976_72000[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71975 === (1))){
var state_71974__$1 = state_71974;
var statearr_71977_72001 = state_71974__$1;
(statearr_71977_72001[(2)] = null);

(statearr_71977_72001[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71975 === (4))){
var state_71974__$1 = state_71974;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71974__$1,(7),org.numenta.sanity.demos.letters.world_c);
} else {
if((state_val_71975 === (6))){
var inst_71963 = (state_71974[(2)]);
var state_71974__$1 = state_71974;
if(cljs.core.truth_(inst_71963)){
var statearr_71978_72002 = state_71974__$1;
(statearr_71978_72002[(1)] = (8));

} else {
var statearr_71979_72003 = state_71974__$1;
(statearr_71979_72003[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_71975 === (3))){
var inst_71972 = (state_71974[(2)]);
var state_71974__$1 = state_71974;
return cljs.core.async.impl.ioc_helpers.return_chan(state_71974__$1,inst_71972);
} else {
if((state_val_71975 === (2))){
var inst_71957 = (state_71974[(7)]);
var inst_71956 = cljs.core.count(org.numenta.sanity.demos.letters.world_buffer);
var inst_71957__$1 = (inst_71956 > (0));
var state_71974__$1 = (function (){var statearr_71980 = state_71974;
(statearr_71980[(7)] = inst_71957__$1);

return statearr_71980;
})();
if(cljs.core.truth_(inst_71957__$1)){
var statearr_71981_72004 = state_71974__$1;
(statearr_71981_72004[(1)] = (4));

} else {
var statearr_71982_72005 = state_71974__$1;
(statearr_71982_72005[(1)] = (5));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_71975 === (9))){
var state_71974__$1 = state_71974;
var statearr_71983_72006 = state_71974__$1;
(statearr_71983_72006[(2)] = null);

(statearr_71983_72006[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71975 === (5))){
var inst_71957 = (state_71974[(7)]);
var state_71974__$1 = state_71974;
var statearr_71984_72007 = state_71974__$1;
(statearr_71984_72007[(2)] = inst_71957);

(statearr_71984_72007[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71975 === (10))){
var inst_71970 = (state_71974[(2)]);
var state_71974__$1 = state_71974;
var statearr_71985_72008 = state_71974__$1;
(statearr_71985_72008[(2)] = inst_71970);

(statearr_71985_72008[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71975 === (8))){
var inst_71965 = cljs.core.count(org.numenta.sanity.demos.letters.world_buffer);
var inst_71966 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.letters.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,inst_71965);
var state_71974__$1 = (function (){var statearr_71986 = state_71974;
(statearr_71986[(8)] = inst_71966);

return statearr_71986;
})();
var statearr_71987_72009 = state_71974__$1;
(statearr_71987_72009[(2)] = null);

(statearr_71987_72009[(1)] = (2));


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
});})(c__38109__auto___71999))
;
return ((function (switch__37995__auto__,c__38109__auto___71999){
return (function() {
var org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto____0 = (function (){
var statearr_71991 = [null,null,null,null,null,null,null,null,null];
(statearr_71991[(0)] = org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto__);

(statearr_71991[(1)] = (1));

return statearr_71991;
});
var org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto____1 = (function (state_71974){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71974);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71992){if((e71992 instanceof Object)){
var ex__37999__auto__ = e71992;
var statearr_71993_72010 = state_71974;
(statearr_71993_72010[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71974);

return cljs.core.cst$kw$recur;
} else {
throw e71992;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__72011 = state_71974;
state_71974 = G__72011;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto__ = function(state_71974){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto____1.call(this,state_71974);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$letters$model_tab_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___71999))
})();
var state__38111__auto__ = (function (){var statearr_71994 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71994[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___71999);

return statearr_71994;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___71999))
);


return e.preventDefault();
})], null),"Clear"], null):null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$well,"Immediate input as you type: ",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$size,(2),cljs.core.cst$kw$maxLength,(1),cljs.core.cst$kw$on_DASH_key_DASH_press,(function (e){
org.numenta.sanity.demos.letters.immediate_key_down_BANG_(e);

return e.preventDefault();
})], null)], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$well,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$textarea,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$width,"90%",cljs.core.cst$kw$height,"10em"], null),cljs.core.cst$kw$value,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.letters.text_to_send) : cljs.core.deref.call(null,org.numenta.sanity.demos.letters.text_to_send)),cljs.core.cst$kw$on_DASH_change,(function (e){
var G__71996_72012 = org.numenta.sanity.demos.letters.text_to_send;
var G__71997_72013 = (function (){var G__71998 = e.target;
return goog.dom.forms.getValue(G__71998);
})();
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__71996_72012,G__71997_72013) : cljs.core.reset_BANG_.call(null,G__71996_72012,G__71997_72013));

return e.preventDefault();
})], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$class,(((cljs.core.count(org.numenta.sanity.demos.letters.world_buffer) > (0)))?"btn-default":"btn-primary"),cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.letters.send_text_BANG_();

return e.preventDefault();
})], null),(((cljs.core.count(org.numenta.sanity.demos.letters.world_buffer) > (0)))?"Queue more text input":"Queue text input")], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"HTM model"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.bind_fields,org.numenta.sanity.demos.letters.config_template,org.numenta.sanity.demos.letters.config], null)], null);
});
org.numenta.sanity.demos.letters.init = (function org$numenta$sanity$demos$letters$init(){
reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,"Comportex",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.letters.model_tab], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.letters.world_pane], null),reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$model),org.numenta.sanity.demos.comportex_common.all_features,org.numenta.sanity.demos.letters.into_sim], null),goog.dom.getElement("sanity-app"));

org.numenta.sanity.demos.letters.send_text_BANG_();

return org.numenta.sanity.demos.letters.set_model_BANG_();
});
goog.exportSymbol('org.numenta.sanity.demos.letters.init', org.numenta.sanity.demos.letters.init);
