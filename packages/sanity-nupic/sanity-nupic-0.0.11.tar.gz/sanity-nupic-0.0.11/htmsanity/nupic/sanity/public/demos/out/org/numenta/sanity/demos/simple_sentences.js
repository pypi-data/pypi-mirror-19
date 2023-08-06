// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.simple_sentences');
goog.require('cljs.core');
goog.require('goog.dom.forms');
goog.require('goog.dom');
goog.require('reagent.core');
goog.require('org.numenta.sanity.helpers');
goog.require('org.numenta.sanity.main');
goog.require('org.nfrac.comportex.demos.simple_sentences');
goog.require('org.numenta.sanity.util');
goog.require('org.numenta.sanity.comportex.data');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('reagent_forms.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.numenta.sanity.bridge.browser');
goog.require('org.numenta.sanity.demos.comportex_common');
goog.require('org.nfrac.comportex.util');
org.numenta.sanity.demos.simple_sentences.config = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$n_DASH_regions,(1),cljs.core.cst$kw$repeats,(1),cljs.core.cst$kw$text,org.nfrac.comportex.demos.simple_sentences.input_text,cljs.core.cst$kw$world_DASH_buffer_DASH_count,(0)], null));
org.numenta.sanity.demos.simple_sentences.world_buffer = cljs.core.async.buffer((5000));
org.numenta.sanity.demos.simple_sentences.world_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.simple_sentences.world_buffer,cljs.core.comp.cljs$core$IFn$_invoke$arity$2(cljs.core.map.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.util.keep_history_middleware((100),cljs.core.cst$kw$word,cljs.core.cst$kw$history)),cljs.core.map.cljs$core$IFn$_invoke$arity$1((function (p1__70582_SHARP_){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__70582_SHARP_,cljs.core.cst$kw$label,cljs.core.cst$kw$word.cljs$core$IFn$_invoke$arity$1(p1__70582_SHARP_));
}))));
org.numenta.sanity.demos.simple_sentences.into_sim = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.demos.simple_sentences.model = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.demos.simple_sentences.model,cljs.core.cst$kw$org$numenta$sanity$demos$simple_DASH_sentences_SLASH_count_DASH_world_DASH_buffer,(function (_,___$1,___$2,___$3){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.simple_sentences.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.count(org.numenta.sanity.demos.simple_sentences.world_buffer));
}));
org.numenta.sanity.demos.simple_sentences.max_shown = (100);
org.numenta.sanity.demos.simple_sentences.scroll_every = (50);
org.numenta.sanity.demos.simple_sentences.world_pane = (function org$numenta$sanity$demos$simple_sentences$world_pane(){
var show_predictions = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(false);
var selected_htm = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.main.selection,cljs.core.cst$kw$org$numenta$sanity$demos$simple_DASH_sentences_SLASH_fetch_DASH_selected_DASH_htm,((function (show_predictions,selected_htm){
return (function (_,___$1,___$2,p__70598){
var vec__70599 = p__70598;
var sel1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70599,(0),null);
var temp__4657__auto__ = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(sel1,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$step,cljs.core.cst$kw$snapshot_DASH_id], null));
if(cljs.core.truth_(temp__4657__auto__)){
var snapshot_id = temp__4657__auto__;
var out_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, ["get-model",snapshot_id,org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(out_c,true)], null));

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__70599,sel1,show_predictions,selected_htm){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__70599,sel1,show_predictions,selected_htm){
return (function (state_70604){
var state_val_70605 = (state_70604[(1)]);
if((state_val_70605 === (1))){
var state_70604__$1 = state_70604;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_70604__$1,(2),out_c);
} else {
if((state_val_70605 === (2))){
var inst_70601 = (state_70604[(2)]);
var inst_70602 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_htm,inst_70601) : cljs.core.reset_BANG_.call(null,selected_htm,inst_70601));
var state_70604__$1 = state_70604;
return cljs.core.async.impl.ioc_helpers.return_chan(state_70604__$1,inst_70602);
} else {
return null;
}
}
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__70599,sel1,show_predictions,selected_htm))
;
return ((function (switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__70599,sel1,show_predictions,selected_htm){
return (function() {
var org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto____0 = (function (){
var statearr_70609 = [null,null,null,null,null,null,null];
(statearr_70609[(0)] = org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto__);

(statearr_70609[(1)] = (1));

return statearr_70609;
});
var org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto____1 = (function (state_70604){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_70604);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e70610){if((e70610 instanceof Object)){
var ex__37999__auto__ = e70610;
var statearr_70611_70613 = state_70604;
(statearr_70611_70613[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_70604);

return cljs.core.cst$kw$recur;
} else {
throw e70610;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__70614 = state_70604;
state_70604 = G__70614;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto__ = function(state_70604){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto____1.call(this,state_70604);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$simple_sentences$world_pane_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__70599,sel1,show_predictions,selected_htm))
})();
var state__38111__auto__ = (function (){var statearr_70612 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_70612[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_70612;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__70599,sel1,show_predictions,selected_htm))
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
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$muted,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Input on selected timestep."], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$min_DASH_height,"40vh"], null)], null),org.numenta.sanity.helpers.text_world_input_component(inval,htm,org.numenta.sanity.demos.simple_sentences.max_shown,org.numenta.sanity.demos.simple_sentences.scroll_every," ")], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$checkbox,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$type,cljs.core.cst$kw$checkbox,cljs.core.cst$kw$checked,(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(show_predictions) : cljs.core.deref.call(null,show_predictions)))?true:null),cljs.core.cst$kw$on_DASH_change,((function (inval,htm,temp__4657__auto__,show_predictions,selected_htm){
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
org.numenta.sanity.demos.simple_sentences.set_model_BANG_ = (function org$numenta$sanity$demos$simple_sentences$set_model_BANG_(){
return org.numenta.sanity.helpers.with_ui_loading_message((function (){
var n_regions = cljs.core.cst$kw$n_DASH_regions.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.simple_sentences.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.simple_sentences.config)));
var init_QMARK_ = ((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.simple_sentences.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.simple_sentences.model)) == null);
var G__70619_70623 = org.numenta.sanity.demos.simple_sentences.model;
var G__70620_70624 = org.nfrac.comportex.demos.simple_sentences.n_region_model.cljs$core$IFn$_invoke$arity$2(n_regions,org.nfrac.comportex.demos.simple_sentences.spec);
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__70619_70623,G__70620_70624) : cljs.core.reset_BANG_.call(null,G__70619_70623,G__70620_70624));

if(init_QMARK_){
return org.numenta.sanity.bridge.browser.init.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.simple_sentences.model,org.numenta.sanity.demos.simple_sentences.world_c,org.numenta.sanity.main.into_journal,org.numenta.sanity.demos.simple_sentences.into_sim);
} else {
var G__70621 = org.numenta.sanity.main.network_shape;
var G__70622 = org.numenta.sanity.util.translate_network_shape(org.numenta.sanity.comportex.data.network_shape((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.simple_sentences.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.simple_sentences.model))));
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__70621,G__70622) : cljs.core.reset_BANG_.call(null,G__70621,G__70622));
}
}));
});
org.numenta.sanity.demos.simple_sentences.send_text_BANG_ = (function org$numenta$sanity$demos$simple_sentences$send_text_BANG_(){
var temp__4657__auto__ = cljs.core.seq(org.nfrac.comportex.demos.simple_sentences.word_item_seq(cljs.core.cst$kw$repeats.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.simple_sentences.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.simple_sentences.config))),cljs.core.cst$kw$text.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.simple_sentences.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.simple_sentences.config)))));
if(temp__4657__auto__){
var xs = temp__4657__auto__;
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,xs,temp__4657__auto__){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,xs,temp__4657__auto__){
return (function (state_70647){
var state_val_70648 = (state_70647[(1)]);
if((state_val_70648 === (1))){
var inst_70641 = cljs.core.async.onto_chan.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.demos.simple_sentences.world_c,xs,false);
var state_70647__$1 = state_70647;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_70647__$1,(2),inst_70641);
} else {
if((state_val_70648 === (2))){
var inst_70643 = (state_70647[(2)]);
var inst_70644 = cljs.core.count(org.numenta.sanity.demos.simple_sentences.world_buffer);
var inst_70645 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.simple_sentences.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,inst_70644);
var state_70647__$1 = (function (){var statearr_70649 = state_70647;
(statearr_70649[(7)] = inst_70643);

return statearr_70649;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_70647__$1,inst_70645);
} else {
return null;
}
}
});})(c__38109__auto__,xs,temp__4657__auto__))
;
return ((function (switch__37995__auto__,c__38109__auto__,xs,temp__4657__auto__){
return (function() {
var org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_70653 = [null,null,null,null,null,null,null,null];
(statearr_70653[(0)] = org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto__);

(statearr_70653[(1)] = (1));

return statearr_70653;
});
var org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto____1 = (function (state_70647){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_70647);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e70654){if((e70654 instanceof Object)){
var ex__37999__auto__ = e70654;
var statearr_70655_70657 = state_70647;
(statearr_70655_70657[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_70647);

return cljs.core.cst$kw$recur;
} else {
throw e70654;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__70658 = state_70647;
state_70647 = G__70658;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto__ = function(state_70647){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto____1.call(this,state_70647);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$simple_sentences$send_text_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,xs,temp__4657__auto__))
})();
var state__38111__auto__ = (function (){var statearr_70656 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_70656[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_70656;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,xs,temp__4657__auto__))
);

return c__38109__auto__;
} else {
return null;
}
});
org.numenta.sanity.demos.simple_sentences.config_template = new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"Input ",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Word sequences"], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_info,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$label,cljs.core.cst$kw$id,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.cst$kw$postamble," queued input values."], null)], null)," ",new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$container,cljs.core.cst$kw$visible_QMARK_,(function (p1__70659_SHARP_){
return (cljs.core.cst$kw$world_DASH_buffer_DASH_count.cljs$core$IFn$_invoke$arity$1(p1__70659_SHARP_) > (0));
})], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_warning$btn_DASH_xs,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
var c__38109__auto___70702 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___70702){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___70702){
return (function (state_70681){
var state_val_70682 = (state_70681[(1)]);
if((state_val_70682 === (7))){
var inst_70667 = (state_70681[(2)]);
var state_70681__$1 = state_70681;
var statearr_70683_70703 = state_70681__$1;
(statearr_70683_70703[(2)] = inst_70667);

(statearr_70683_70703[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70682 === (1))){
var state_70681__$1 = state_70681;
var statearr_70684_70704 = state_70681__$1;
(statearr_70684_70704[(2)] = null);

(statearr_70684_70704[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70682 === (4))){
var state_70681__$1 = state_70681;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_70681__$1,(7),org.numenta.sanity.demos.simple_sentences.world_c);
} else {
if((state_val_70682 === (6))){
var inst_70670 = (state_70681[(2)]);
var state_70681__$1 = state_70681;
if(cljs.core.truth_(inst_70670)){
var statearr_70685_70705 = state_70681__$1;
(statearr_70685_70705[(1)] = (8));

} else {
var statearr_70686_70706 = state_70681__$1;
(statearr_70686_70706[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_70682 === (3))){
var inst_70679 = (state_70681[(2)]);
var state_70681__$1 = state_70681;
return cljs.core.async.impl.ioc_helpers.return_chan(state_70681__$1,inst_70679);
} else {
if((state_val_70682 === (2))){
var inst_70664 = (state_70681[(7)]);
var inst_70663 = cljs.core.count(org.numenta.sanity.demos.simple_sentences.world_buffer);
var inst_70664__$1 = (inst_70663 > (0));
var state_70681__$1 = (function (){var statearr_70687 = state_70681;
(statearr_70687[(7)] = inst_70664__$1);

return statearr_70687;
})();
if(cljs.core.truth_(inst_70664__$1)){
var statearr_70688_70707 = state_70681__$1;
(statearr_70688_70707[(1)] = (4));

} else {
var statearr_70689_70708 = state_70681__$1;
(statearr_70689_70708[(1)] = (5));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_70682 === (9))){
var state_70681__$1 = state_70681;
var statearr_70690_70709 = state_70681__$1;
(statearr_70690_70709[(2)] = null);

(statearr_70690_70709[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70682 === (5))){
var inst_70664 = (state_70681[(7)]);
var state_70681__$1 = state_70681;
var statearr_70691_70710 = state_70681__$1;
(statearr_70691_70710[(2)] = inst_70664);

(statearr_70691_70710[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70682 === (10))){
var inst_70677 = (state_70681[(2)]);
var state_70681__$1 = state_70681;
var statearr_70692_70711 = state_70681__$1;
(statearr_70692_70711[(2)] = inst_70677);

(statearr_70692_70711[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70682 === (8))){
var inst_70672 = cljs.core.count(org.numenta.sanity.demos.simple_sentences.world_buffer);
var inst_70673 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.simple_sentences.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,inst_70672);
var state_70681__$1 = (function (){var statearr_70693 = state_70681;
(statearr_70693[(8)] = inst_70673);

return statearr_70693;
})();
var statearr_70694_70712 = state_70681__$1;
(statearr_70694_70712[(2)] = null);

(statearr_70694_70712[(1)] = (2));


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
});})(c__38109__auto___70702))
;
return ((function (switch__37995__auto__,c__38109__auto___70702){
return (function() {
var org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto____0 = (function (){
var statearr_70698 = [null,null,null,null,null,null,null,null,null];
(statearr_70698[(0)] = org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto__);

(statearr_70698[(1)] = (1));

return statearr_70698;
});
var org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto____1 = (function (state_70681){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_70681);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e70699){if((e70699 instanceof Object)){
var ex__37999__auto__ = e70699;
var statearr_70700_70713 = state_70681;
(statearr_70700_70713[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_70681);

return cljs.core.cst$kw$recur;
} else {
throw e70699;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__70714 = state_70681;
state_70681 = G__70714;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto__ = function(state_70681){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto____1.call(this,state_70681);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto____0;
org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto____1;
return org$numenta$sanity$demos$simple_sentences$state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___70702))
})();
var state__38111__auto__ = (function (){var statearr_70701 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_70701[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___70702);

return statearr_70701;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___70702))
);


return e.preventDefault();
})], null),"Clear"], null)], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Repeats of each sentence:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$repeats], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_12,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$textarea$form_DASH_control,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$textarea,cljs.core.cst$kw$id,cljs.core.cst$kw$text,cljs.core.cst$kw$rows,(10)], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_8,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_primary,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$container,cljs.core.cst$kw$visible_QMARK_,(function (p1__70660_SHARP_){
return (cljs.core.cst$kw$world_DASH_buffer_DASH_count.cljs$core$IFn$_invoke$arity$1(p1__70660_SHARP_) === (0));
}),cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.simple_sentences.send_text_BANG_();

return e.preventDefault();
})], null),"Queue text input"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$container,cljs.core.cst$kw$visible_QMARK_,(function (p1__70661_SHARP_){
return (cljs.core.cst$kw$world_DASH_buffer_DASH_count.cljs$core$IFn$_invoke$arity$1(p1__70661_SHARP_) > (0));
}),cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.simple_sentences.send_text_BANG_();

return e.preventDefault();
})], null),"Queue more text input"], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"HTM model"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Number of regions:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$n_DASH_regions], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_offset_DASH_5$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.simple_sentences.set_model_BANG_();

return e.preventDefault();
})], null),"Restart with new model"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_danger,"This resets all parameters."], null)], null)], null)], null)], null);
org.numenta.sanity.demos.simple_sentences.model_tab = (function org$numenta$sanity$demos$simple_sentences$model_tab(){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"In this example, text is presented as a sequence of words,\n        with independent unique encodings. The text is split into\n        sentences at each period (.) and each sentence into\n        words."], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.bind_fields,org.numenta.sanity.demos.simple_sentences.config_template,org.numenta.sanity.demos.simple_sentences.config], null)], null);
});
org.numenta.sanity.demos.simple_sentences.init = (function org$numenta$sanity$demos$simple_sentences$init(){
reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,"Comportex",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.simple_sentences.model_tab], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.simple_sentences.world_pane], null),reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$model),org.numenta.sanity.demos.comportex_common.all_features,org.numenta.sanity.demos.simple_sentences.into_sim], null),goog.dom.getElement("sanity-app"));

org.numenta.sanity.demos.simple_sentences.send_text_BANG_();

return org.numenta.sanity.demos.simple_sentences.set_model_BANG_();
});
goog.exportSymbol('org.numenta.sanity.demos.simple_sentences.init', org.numenta.sanity.demos.simple_sentences.init);
