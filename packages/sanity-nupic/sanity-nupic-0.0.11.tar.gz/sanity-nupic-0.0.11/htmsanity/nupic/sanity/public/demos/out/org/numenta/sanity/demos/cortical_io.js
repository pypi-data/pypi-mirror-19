// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.cortical_io');
goog.require('cljs.core');
goog.require('goog.dom.forms');
goog.require('goog.dom');
goog.require('reagent.core');
goog.require('org.numenta.sanity.helpers');
goog.require('org.numenta.sanity.main');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.numenta.sanity.util');
goog.require('org.numenta.sanity.comportex.data');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('reagent_forms.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.numenta.sanity.bridge.browser');
goog.require('org.nfrac.comportex.cortical_io');
goog.require('org.numenta.sanity.demos.comportex_common');
goog.require('org.nfrac.comportex.util');
goog.require('org.nfrac.comportex.encoders');
goog.require('clojure.string');
org.numenta.sanity.demos.cortical_io.fox_eats_what = "\nfrog eat flies.\ncow eat grain.\nelephant eat leaves.\ngoat eat grass.\nwolf eat rabbit.\ncat likes ball.\nelephant likes water.\nsheep eat grass.\ncat eat salmon.\nwolf eat mice.\nlion eat cow.\ndog likes sleep.\ncoyote eat mice.\ncoyote eat rodent.\ncoyote eat rabbit.\nwolf eat squirrel.\ncow eat grass.\nfrog eat flies.\ncow eat grain.\nelephant eat leaves.\ngoat eat grass.\nwolf eat rabbit.\nsheep eat grass.\ncat eat salmon.\nwolf eat mice.\nlion eat cow.\ncoyote eat mice.\nelephant likes water.\ncat likes ball.\ncoyote eat rodent.\ncoyote eat rabbit.\nwolf eat squirrel.\ndog likes sleep.\ncat eat salmon.\ncat likes ball.\ncow eat grass.\nfox eat something.\n";
org.numenta.sanity.demos.cortical_io.fingerprint_cache = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.PersistentArrayMap.EMPTY);
org.numenta.sanity.demos.cortical_io.config = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.PersistentHashMap.fromArrays([cljs.core.cst$kw$decode_DASH_locally_QMARK_,cljs.core.cst$kw$cache_DASH_count,cljs.core.cst$kw$repeats,cljs.core.cst$kw$spec_DASH_choice,cljs.core.cst$kw$spatial_DASH_scramble_QMARK_,cljs.core.cst$kw$encoder,cljs.core.cst$kw$have_DASH_model_QMARK_,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.cst$kw$n_DASH_regions,cljs.core.cst$kw$api_DASH_key,cljs.core.cst$kw$text],[true,(0),(3),cljs.core.cst$kw$a,false,cljs.core.cst$kw$cortical_DASH_io,false,(0),(1),null,org.numenta.sanity.demos.cortical_io.fox_eats_what]));
org.numenta.sanity.demos.cortical_io.world_buffer = cljs.core.async.buffer((5000));
org.numenta.sanity.demos.cortical_io.world_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.cortical_io.world_buffer,cljs.core.comp.cljs$core$IFn$_invoke$arity$2(cljs.core.map.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.util.keep_history_middleware((100),cljs.core.cst$kw$word,cljs.core.cst$kw$history)),cljs.core.map.cljs$core$IFn$_invoke$arity$1((function (p1__73657_SHARP_){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__73657_SHARP_,cljs.core.cst$kw$label,cljs.core.cst$kw$word.cljs$core$IFn$_invoke$arity$1(p1__73657_SHARP_));
}))));
org.numenta.sanity.demos.cortical_io.into_sim = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.demos.cortical_io.model = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.demos.cortical_io.model,cljs.core.cst$kw$org$numenta$sanity$demos$cortical_DASH_io_SLASH_count_DASH_world_DASH_buffer,(function (_,___$1,___$2,___$3){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.cortical_io.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.count(org.numenta.sanity.demos.cortical_io.world_buffer));
}));
cljs.core.add_watch(org.numenta.sanity.demos.cortical_io.fingerprint_cache,cljs.core.cst$kw$count,(function (_,___$1,___$2,v){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.cortical_io.config,cljs.core.assoc,cljs.core.cst$kw$cache_DASH_count,cljs.core.count(v));
}));
org.numenta.sanity.demos.cortical_io.spec_global = cljs.core.PersistentHashMap.fromArrays([cljs.core.cst$kw$column_DASH_dimensions,cljs.core.cst$kw$distal_DASH_vs_DASH_proximal_DASH_weight,cljs.core.cst$kw$ff_DASH_init_DASH_frac,cljs.core.cst$kw$distal,cljs.core.cst$kw$max_DASH_boost,cljs.core.cst$kw$ff_DASH_potential_DASH_radius,cljs.core.cst$kw$activation_DASH_level,cljs.core.cst$kw$proximal,cljs.core.cst$kw$depth,cljs.core.cst$kw$duty_DASH_cycle_DASH_period],[new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(30),(40)], null),(0),0.2,cljs.core.PersistentHashMap.fromArrays([cljs.core.cst$kw$perm_DASH_connected,cljs.core.cst$kw$max_DASH_synapse_DASH_count,cljs.core.cst$kw$max_DASH_segments,cljs.core.cst$kw$perm_DASH_init,cljs.core.cst$kw$new_DASH_synapse_DASH_count,cljs.core.cst$kw$stimulus_DASH_threshold,cljs.core.cst$kw$punish_QMARK_,cljs.core.cst$kw$perm_DASH_dec,cljs.core.cst$kw$learn_DASH_threshold,cljs.core.cst$kw$perm_DASH_inc],[0.2,(18),(5),0.16,(12),(9),true,0.01,(6),0.05]),2.0,1.0,0.02,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$perm_DASH_inc,0.05,cljs.core.cst$kw$perm_DASH_dec,0.005,cljs.core.cst$kw$perm_DASH_connected,0.2,cljs.core.cst$kw$stimulus_DASH_threshold,(1)], null),(5),(100000)]);
org.numenta.sanity.demos.cortical_io.spec_local = cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(org.numenta.sanity.demos.cortical_io.spec_global,cljs.core.cst$kw$ff_DASH_init_DASH_frac,0.3,cljs.core.array_seq([cljs.core.cst$kw$ff_DASH_potential_DASH_radius,0.2,cljs.core.cst$kw$spatial_DASH_pooling,cljs.core.cst$kw$local_DASH_inhibition,cljs.core.cst$kw$inhibition_DASH_base_DASH_distance,(1)], 0));
org.numenta.sanity.demos.cortical_io.higher_level_spec_diff = new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(300)], null)], null);
org.numenta.sanity.demos.cortical_io.load_predictions = (function org$numenta$sanity$demos$cortical_io$load_predictions(htm,n_predictions,predictions_cache){
var vec__73672 = cljs.core.first(cljs.core.vals(cljs.core.cst$kw$sensors.cljs$core$IFn$_invoke$arity$1(htm)));
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73672,(0),null);
var e = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73672,(1),null);
var rgn = cljs.core.first(org.nfrac.comportex.core.region_seq(htm));
var pr_votes = org.nfrac.comportex.core.predicted_bit_votes(rgn);
var predictions = org.nfrac.comportex.protocols.decode(e,pr_votes,n_predictions);
var temp__4655__auto__ = cljs.core.cst$kw$channel.cljs$core$IFn$_invoke$arity$1(predictions);
if(cljs.core.truth_(temp__4655__auto__)){
var c = temp__4655__auto__;
var c__38109__auto___73686 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___73686,c,temp__4655__auto__,vec__73672,_,e,rgn,pr_votes,predictions){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___73686,c,temp__4655__auto__,vec__73672,_,e,rgn,pr_votes,predictions){
return (function (state_73677){
var state_val_73678 = (state_73677[(1)]);
if((state_val_73678 === (1))){
var state_73677__$1 = state_73677;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73677__$1,(2),c);
} else {
if((state_val_73678 === (2))){
var inst_73674 = (state_73677[(2)]);
var inst_73675 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(predictions_cache,cljs.core.assoc,htm,inst_73674);
var state_73677__$1 = state_73677;
return cljs.core.async.impl.ioc_helpers.return_chan(state_73677__$1,inst_73675);
} else {
return null;
}
}
});})(c__38109__auto___73686,c,temp__4655__auto__,vec__73672,_,e,rgn,pr_votes,predictions))
;
return ((function (switch__37995__auto__,c__38109__auto___73686,c,temp__4655__auto__,vec__73672,_,e,rgn,pr_votes,predictions){
return (function() {
var org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto____0 = (function (){
var statearr_73682 = [null,null,null,null,null,null,null];
(statearr_73682[(0)] = org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto__);

(statearr_73682[(1)] = (1));

return statearr_73682;
});
var org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto____1 = (function (state_73677){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_73677);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e73683){if((e73683 instanceof Object)){
var ex__37999__auto__ = e73683;
var statearr_73684_73687 = state_73677;
(statearr_73684_73687[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_73677);

return cljs.core.cst$kw$recur;
} else {
throw e73683;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__73688 = state_73677;
state_73677 = G__73688;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto__ = function(state_73677){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto____1.call(this,state_73677);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$cortical_io$load_predictions_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___73686,c,temp__4655__auto__,vec__73672,_,e,rgn,pr_votes,predictions))
})();
var state__38111__auto__ = (function (){var statearr_73685 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_73685[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___73686);

return statearr_73685;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___73686,c,temp__4655__auto__,vec__73672,_,e,rgn,pr_votes,predictions))
);


return null;
} else {
return predictions;
}
});
org.numenta.sanity.demos.cortical_io.max_shown = (100);
org.numenta.sanity.demos.cortical_io.scroll_every = (50);
org.numenta.sanity.demos.cortical_io.world_pane = (function org$numenta$sanity$demos$cortical_io$world_pane(){
var show_predictions = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(false);
var predictions_cache = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.PersistentArrayMap.EMPTY);
var selected_htm = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.main.selection,cljs.core.cst$kw$org$numenta$sanity$demos$cortical_DASH_io_SLASH_fetch_DASH_selected_DASH_htm,((function (show_predictions,predictions_cache,selected_htm){
return (function (_,___$1,___$2,p__73704){
var vec__73705 = p__73704;
var sel1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73705,(0),null);
var temp__4657__auto__ = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(sel1,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$step,cljs.core.cst$kw$snapshot_DASH_id], null));
if(cljs.core.truth_(temp__4657__auto__)){
var snapshot_id = temp__4657__auto__;
var out_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, ["get-model",snapshot_id,org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$1(out_c)], null));

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__73705,sel1,show_predictions,predictions_cache,selected_htm){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__73705,sel1,show_predictions,predictions_cache,selected_htm){
return (function (state_73710){
var state_val_73711 = (state_73710[(1)]);
if((state_val_73711 === (1))){
var state_73710__$1 = state_73710;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73710__$1,(2),out_c);
} else {
if((state_val_73711 === (2))){
var inst_73707 = (state_73710[(2)]);
var inst_73708 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_htm,inst_73707) : cljs.core.reset_BANG_.call(null,selected_htm,inst_73707));
var state_73710__$1 = state_73710;
return cljs.core.async.impl.ioc_helpers.return_chan(state_73710__$1,inst_73708);
} else {
return null;
}
}
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__73705,sel1,show_predictions,predictions_cache,selected_htm))
;
return ((function (switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__73705,sel1,show_predictions,predictions_cache,selected_htm){
return (function() {
var org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto____0 = (function (){
var statearr_73715 = [null,null,null,null,null,null,null];
(statearr_73715[(0)] = org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto__);

(statearr_73715[(1)] = (1));

return statearr_73715;
});
var org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto____1 = (function (state_73710){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_73710);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e73716){if((e73716 instanceof Object)){
var ex__37999__auto__ = e73716;
var statearr_73717_73719 = state_73710;
(statearr_73717_73719[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_73710);

return cljs.core.cst$kw$recur;
} else {
throw e73716;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__73720 = state_73710;
state_73710 = G__73720;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto__ = function(state_73710){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto____1.call(this,state_73710);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$cortical_io$world_pane_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__73705,sel1,show_predictions,predictions_cache,selected_htm))
})();
var state__38111__auto__ = (function (){var statearr_73718 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_73718[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_73718;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__73705,sel1,show_predictions,predictions_cache,selected_htm))
);

return c__38109__auto__;
} else {
return null;
}
});})(show_predictions,predictions_cache,selected_htm))
);

return ((function (show_predictions,predictions_cache,selected_htm){
return (function (){
var temp__4657__auto__ = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_htm) : cljs.core.deref.call(null,selected_htm));
if(cljs.core.truth_(temp__4657__auto__)){
var htm = temp__4657__auto__;
var inval = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(htm);
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$muted,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Input on selected timestep."], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$min_DASH_height,"40vh"], null)], null),org.numenta.sanity.helpers.text_world_input_component(inval,htm,org.numenta.sanity.demos.cortical_io.max_shown,org.numenta.sanity.demos.cortical_io.scroll_every," ")], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default$btn_DASH_block,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$class,(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(show_predictions) : cljs.core.deref.call(null,show_predictions)))?"active":null),cljs.core.cst$kw$on_DASH_click,((function (inval,htm,temp__4657__auto__,show_predictions,predictions_cache,selected_htm){
return (function (e){
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(show_predictions,cljs.core.not);

return e.preventDefault();
});})(inval,htm,temp__4657__auto__,show_predictions,predictions_cache,selected_htm))
], null),"Compute predictions"], null)], null),(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(show_predictions) : cljs.core.deref.call(null,show_predictions)))?(function (){var temp__4655__auto__ = (function (){var or__6153__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(predictions_cache) : cljs.core.deref.call(null,predictions_cache)),htm);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return org.numenta.sanity.demos.cortical_io.load_predictions(htm,(8),predictions_cache);
}
})();
if(cljs.core.truth_(temp__4655__auto__)){
var predictions = temp__4655__auto__;
return org.numenta.sanity.helpers.predictions_table(predictions);
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_info,"Loading predictions..."], null);
}
})():null)], null);
} else {
return null;
}
});
;})(show_predictions,predictions_cache,selected_htm))
});
org.numenta.sanity.demos.cortical_io.split_sentences = (function org$numenta$sanity$demos$cortical_io$split_sentences(text){
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2((function (p1__73722_SHARP_){
return cljs.core.conj.cljs$core$IFn$_invoke$arity$2(p1__73722_SHARP_,".");
}),cljs.core.mapv.cljs$core$IFn$_invoke$arity$2((function (p1__73721_SHARP_){
return clojure.string.split.cljs$core$IFn$_invoke$arity$2(p1__73721_SHARP_,/[^\w']+/);
}),clojure.string.split.cljs$core$IFn$_invoke$arity$2(clojure.string.trim(text),/[^\w]*[\.\!\?]+[^\w]*/)));
});
/**
 * An input sequence consisting of words from the given text, with
 * periods separating sentences also included as distinct words. Each
 * sequence element has the form `{:word _, :index [i j]}`, where i is
 * the sentence index and j is the word index into sentence j.
 */
org.numenta.sanity.demos.cortical_io.word_item_seq = (function org$numenta$sanity$demos$cortical_io$word_item_seq(n_repeats,text){
var iter__6925__auto__ = (function org$numenta$sanity$demos$cortical_io$word_item_seq_$_iter__73760(s__73761){
return (new cljs.core.LazySeq(null,(function (){
var s__73761__$1 = s__73761;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__73761__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var vec__73783 = cljs.core.first(xs__5205__auto__);
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73783,(0),null);
var sen = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73783,(1),null);
var iterys__6921__auto__ = ((function (s__73761__$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function org$numenta$sanity$demos$cortical_io$word_item_seq_$_iter__73760_$_iter__73762(s__73763){
return (new cljs.core.LazySeq(null,((function (s__73761__$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function (){
var s__73763__$1 = s__73763;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__73763__$1);
if(temp__4657__auto____$1){
var xs__5205__auto____$1 = temp__4657__auto____$1;
var rep = cljs.core.first(xs__5205__auto____$1);
var iterys__6921__auto__ = ((function (s__73763__$1,s__73761__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function org$numenta$sanity$demos$cortical_io$word_item_seq_$_iter__73760_$_iter__73762_$_iter__73764(s__73765){
return (new cljs.core.LazySeq(null,((function (s__73763__$1,s__73761__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__){
return (function (){
var s__73765__$1 = s__73765;
while(true){
var temp__4657__auto____$2 = cljs.core.seq(s__73765__$1);
if(temp__4657__auto____$2){
var s__73765__$2 = temp__4657__auto____$2;
if(cljs.core.chunked_seq_QMARK_(s__73765__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__73765__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__73767 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__73766 = (0);
while(true){
if((i__73766 < size__6924__auto__)){
var vec__73795 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__73766);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73795,(0),null);
var word = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73795,(1),null);
cljs.core.chunk_append(b__73767,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$word,word,cljs.core.cst$kw$index,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,j], null)], null));

var G__73797 = (i__73766 + (1));
i__73766 = G__73797;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__73767),org$numenta$sanity$demos$cortical_io$word_item_seq_$_iter__73760_$_iter__73762_$_iter__73764(cljs.core.chunk_rest(s__73765__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__73767),null);
}
} else {
var vec__73796 = cljs.core.first(s__73765__$2);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73796,(0),null);
var word = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73796,(1),null);
return cljs.core.cons(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$word,word,cljs.core.cst$kw$index,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,j], null)], null),org$numenta$sanity$demos$cortical_io$word_item_seq_$_iter__73760_$_iter__73762_$_iter__73764(cljs.core.rest(s__73765__$2)));
}
} else {
return null;
}
break;
}
});})(s__73763__$1,s__73761__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__))
,null,null));
});})(s__73763__$1,s__73761__$1,rep,xs__5205__auto____$1,temp__4657__auto____$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,sen)));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$numenta$sanity$demos$cortical_io$word_item_seq_$_iter__73760_$_iter__73762(cljs.core.rest(s__73763__$1)));
} else {
var G__73798 = cljs.core.rest(s__73763__$1);
s__73763__$1 = G__73798;
continue;
}
} else {
return null;
}
break;
}
});})(s__73761__$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__))
,null,null));
});})(s__73761__$1,vec__73783,i,sen,xs__5205__auto__,temp__4657__auto__))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1(n_repeats)));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$numenta$sanity$demos$cortical_io$word_item_seq_$_iter__73760(cljs.core.rest(s__73761__$1)));
} else {
var G__73799 = cljs.core.rest(s__73761__$1);
s__73761__$1 = G__73799;
continue;
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,org.numenta.sanity.demos.cortical_io.split_sentences(text)));
});
/**
 * Kicks off the process to load the fingerprints.
 */
org.numenta.sanity.demos.cortical_io.cio_start_requests_BANG_ = (function org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG_(api_key,text){
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__){
return (function (state_73935){
var state_val_73936 = (state_73935[(1)]);
if((state_val_73936 === (7))){
var inst_73893 = (state_73935[(7)]);
var inst_73896 = (state_73935[(8)]);
var inst_73895 = (state_73935[(9)]);
var inst_73894 = (state_73935[(10)]);
var inst_73905 = (state_73935[(2)]);
var inst_73906 = (inst_73896 + (1));
var tmp73937 = inst_73893;
var tmp73938 = inst_73895;
var tmp73939 = inst_73894;
var inst_73893__$1 = tmp73937;
var inst_73894__$1 = tmp73939;
var inst_73895__$1 = tmp73938;
var inst_73896__$1 = inst_73906;
var state_73935__$1 = (function (){var statearr_73940 = state_73935;
(statearr_73940[(7)] = inst_73893__$1);

(statearr_73940[(8)] = inst_73896__$1);

(statearr_73940[(9)] = inst_73895__$1);

(statearr_73940[(11)] = inst_73905);

(statearr_73940[(10)] = inst_73894__$1);

return statearr_73940;
})();
var statearr_73941_73968 = state_73935__$1;
(statearr_73941_73968[(2)] = null);

(statearr_73941_73968[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (1))){
var inst_73888 = clojure.string.lower_case(text);
var inst_73889 = org.numenta.sanity.demos.cortical_io.split_sentences(inst_73888);
var inst_73890 = cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.concat,inst_73889);
var inst_73891 = cljs.core.distinct.cljs$core$IFn$_invoke$arity$1(inst_73890);
var inst_73892 = cljs.core.seq(inst_73891);
var inst_73893 = inst_73892;
var inst_73894 = null;
var inst_73895 = (0);
var inst_73896 = (0);
var state_73935__$1 = (function (){var statearr_73942 = state_73935;
(statearr_73942[(7)] = inst_73893);

(statearr_73942[(8)] = inst_73896);

(statearr_73942[(9)] = inst_73895);

(statearr_73942[(10)] = inst_73894);

return statearr_73942;
})();
var statearr_73943_73969 = state_73935__$1;
(statearr_73943_73969[(2)] = null);

(statearr_73943_73969[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (4))){
var inst_73896 = (state_73935[(8)]);
var inst_73894 = (state_73935[(10)]);
var inst_73901 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(inst_73894,inst_73896);
var inst_73902 = cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["requesting fingerprint for:",inst_73901], 0));
var inst_73903 = org.nfrac.comportex.cortical_io.cache_fingerprint_BANG_(api_key,org.numenta.sanity.demos.cortical_io.fingerprint_cache,inst_73901);
var state_73935__$1 = (function (){var statearr_73944 = state_73935;
(statearr_73944[(12)] = inst_73902);

return statearr_73944;
})();
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73935__$1,(7),inst_73903);
} else {
if((state_val_73936 === (13))){
var inst_73926 = (state_73935[(2)]);
var state_73935__$1 = state_73935;
var statearr_73945_73970 = state_73935__$1;
(statearr_73945_73970[(2)] = inst_73926);

(statearr_73945_73970[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (6))){
var inst_73931 = (state_73935[(2)]);
var state_73935__$1 = state_73935;
var statearr_73946_73971 = state_73935__$1;
(statearr_73946_73971[(2)] = inst_73931);

(statearr_73946_73971[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (3))){
var inst_73933 = (state_73935[(2)]);
var state_73935__$1 = state_73935;
return cljs.core.async.impl.ioc_helpers.return_chan(state_73935__$1,inst_73933);
} else {
if((state_val_73936 === (12))){
var inst_73909 = (state_73935[(13)]);
var inst_73918 = cljs.core.first(inst_73909);
var inst_73919 = cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["requesting fingerprint for:",inst_73918], 0));
var inst_73920 = org.nfrac.comportex.cortical_io.cache_fingerprint_BANG_(api_key,org.numenta.sanity.demos.cortical_io.fingerprint_cache,inst_73918);
var state_73935__$1 = (function (){var statearr_73947 = state_73935;
(statearr_73947[(14)] = inst_73919);

return statearr_73947;
})();
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73935__$1,(14),inst_73920);
} else {
if((state_val_73936 === (2))){
var inst_73896 = (state_73935[(8)]);
var inst_73895 = (state_73935[(9)]);
var inst_73898 = (inst_73896 < inst_73895);
var inst_73899 = inst_73898;
var state_73935__$1 = state_73935;
if(cljs.core.truth_(inst_73899)){
var statearr_73948_73972 = state_73935__$1;
(statearr_73948_73972[(1)] = (4));

} else {
var statearr_73949_73973 = state_73935__$1;
(statearr_73949_73973[(1)] = (5));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (11))){
var inst_73909 = (state_73935[(13)]);
var inst_73913 = cljs.core.chunk_first(inst_73909);
var inst_73914 = cljs.core.chunk_rest(inst_73909);
var inst_73915 = cljs.core.count(inst_73913);
var inst_73893 = inst_73914;
var inst_73894 = inst_73913;
var inst_73895 = inst_73915;
var inst_73896 = (0);
var state_73935__$1 = (function (){var statearr_73950 = state_73935;
(statearr_73950[(7)] = inst_73893);

(statearr_73950[(8)] = inst_73896);

(statearr_73950[(9)] = inst_73895);

(statearr_73950[(10)] = inst_73894);

return statearr_73950;
})();
var statearr_73951_73974 = state_73935__$1;
(statearr_73951_73974[(2)] = null);

(statearr_73951_73974[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (9))){
var state_73935__$1 = state_73935;
var statearr_73952_73975 = state_73935__$1;
(statearr_73952_73975[(2)] = null);

(statearr_73952_73975[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (5))){
var inst_73893 = (state_73935[(7)]);
var inst_73909 = (state_73935[(13)]);
var inst_73909__$1 = cljs.core.seq(inst_73893);
var state_73935__$1 = (function (){var statearr_73953 = state_73935;
(statearr_73953[(13)] = inst_73909__$1);

return statearr_73953;
})();
if(inst_73909__$1){
var statearr_73954_73976 = state_73935__$1;
(statearr_73954_73976[(1)] = (8));

} else {
var statearr_73955_73977 = state_73935__$1;
(statearr_73955_73977[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (14))){
var inst_73909 = (state_73935[(13)]);
var inst_73922 = (state_73935[(2)]);
var inst_73923 = cljs.core.next(inst_73909);
var inst_73893 = inst_73923;
var inst_73894 = null;
var inst_73895 = (0);
var inst_73896 = (0);
var state_73935__$1 = (function (){var statearr_73956 = state_73935;
(statearr_73956[(7)] = inst_73893);

(statearr_73956[(8)] = inst_73896);

(statearr_73956[(9)] = inst_73895);

(statearr_73956[(15)] = inst_73922);

(statearr_73956[(10)] = inst_73894);

return statearr_73956;
})();
var statearr_73957_73978 = state_73935__$1;
(statearr_73957_73978[(2)] = null);

(statearr_73957_73978[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (10))){
var inst_73929 = (state_73935[(2)]);
var state_73935__$1 = state_73935;
var statearr_73958_73979 = state_73935__$1;
(statearr_73958_73979[(2)] = inst_73929);

(statearr_73958_73979[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73936 === (8))){
var inst_73909 = (state_73935[(13)]);
var inst_73911 = cljs.core.chunked_seq_QMARK_(inst_73909);
var state_73935__$1 = state_73935;
if(inst_73911){
var statearr_73959_73980 = state_73935__$1;
(statearr_73959_73980[(1)] = (11));

} else {
var statearr_73960_73981 = state_73935__$1;
(statearr_73960_73981[(1)] = (12));

}

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
}
}
}
});})(c__38109__auto__))
;
return ((function (switch__37995__auto__,c__38109__auto__){
return (function() {
var org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_73964 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_73964[(0)] = org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto__);

(statearr_73964[(1)] = (1));

return statearr_73964;
});
var org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto____1 = (function (state_73935){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_73935);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e73965){if((e73965 instanceof Object)){
var ex__37999__auto__ = e73965;
var statearr_73966_73982 = state_73935;
(statearr_73966_73982[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_73935);

return cljs.core.cst$kw$recur;
} else {
throw e73965;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__73983 = state_73935;
state_73935 = G__73983;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto__ = function(state_73935){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto____1.call(this,state_73935);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$cortical_io$cio_start_requests_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__))
})();
var state__38111__auto__ = (function (){var statearr_73967 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_73967[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_73967;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__))
);

return c__38109__auto__;
});
org.numenta.sanity.demos.cortical_io.send_text_BANG_ = (function org$numenta$sanity$demos$cortical_io$send_text_BANG_(){
var temp__4657__auto__ = cljs.core.seq(org.numenta.sanity.demos.cortical_io.word_item_seq(cljs.core.cst$kw$repeats.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))),cljs.core.cst$kw$text.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config)))));
if(temp__4657__auto__){
var xs = temp__4657__auto__;
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,xs,temp__4657__auto__){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,xs,temp__4657__auto__){
return (function (state_74037){
var state_val_74038 = (state_74037[(1)]);
if((state_val_74038 === (1))){
var inst_74018 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config));
var inst_74019 = cljs.core.cst$kw$encoder.cljs$core$IFn$_invoke$arity$1(inst_74018);
var inst_74020 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$cortical_DASH_io,inst_74019);
var state_74037__$1 = state_74037;
if(inst_74020){
var statearr_74039_74052 = state_74037__$1;
(statearr_74039_74052[(1)] = (2));

} else {
var statearr_74040_74053 = state_74037__$1;
(statearr_74040_74053[(1)] = (3));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_74038 === (2))){
var inst_74022 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config));
var inst_74023 = cljs.core.cst$kw$api_DASH_key.cljs$core$IFn$_invoke$arity$1(inst_74022);
var inst_74024 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config));
var inst_74025 = cljs.core.cst$kw$text.cljs$core$IFn$_invoke$arity$1(inst_74024);
var inst_74026 = org.numenta.sanity.demos.cortical_io.cio_start_requests_BANG_(inst_74023,inst_74025);
var inst_74027 = cljs.core.async.timeout((2500));
var state_74037__$1 = (function (){var statearr_74041 = state_74037;
(statearr_74041[(7)] = inst_74026);

return statearr_74041;
})();
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_74037__$1,(5),inst_74027);
} else {
if((state_val_74038 === (3))){
var state_74037__$1 = state_74037;
var statearr_74042_74054 = state_74037__$1;
(statearr_74042_74054[(2)] = null);

(statearr_74042_74054[(1)] = (4));


return cljs.core.cst$kw$recur;
} else {
if((state_val_74038 === (4))){
var inst_74032 = (state_74037[(2)]);
var inst_74033 = cljs.core.async.onto_chan.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.demos.cortical_io.world_c,xs,false);
var inst_74034 = cljs.core.count(org.numenta.sanity.demos.cortical_io.world_buffer);
var inst_74035 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.cortical_io.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,inst_74034);
var state_74037__$1 = (function (){var statearr_74043 = state_74037;
(statearr_74043[(8)] = inst_74033);

(statearr_74043[(9)] = inst_74032);

return statearr_74043;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_74037__$1,inst_74035);
} else {
if((state_val_74038 === (5))){
var inst_74029 = (state_74037[(2)]);
var state_74037__$1 = state_74037;
var statearr_74044_74055 = state_74037__$1;
(statearr_74044_74055[(2)] = inst_74029);

(statearr_74044_74055[(1)] = (4));


return cljs.core.cst$kw$recur;
} else {
return null;
}
}
}
}
}
});})(c__38109__auto__,xs,temp__4657__auto__))
;
return ((function (switch__37995__auto__,c__38109__auto__,xs,temp__4657__auto__){
return (function() {
var org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_74048 = [null,null,null,null,null,null,null,null,null,null];
(statearr_74048[(0)] = org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto__);

(statearr_74048[(1)] = (1));

return statearr_74048;
});
var org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto____1 = (function (state_74037){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_74037);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e74049){if((e74049 instanceof Object)){
var ex__37999__auto__ = e74049;
var statearr_74050_74056 = state_74037;
(statearr_74050_74056[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_74037);

return cljs.core.cst$kw$recur;
} else {
throw e74049;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__74057 = state_74037;
state_74037 = G__74057;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto__ = function(state_74037){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto____1.call(this,state_74037);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$cortical_io$send_text_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,xs,temp__4657__auto__))
})();
var state__38111__auto__ = (function (){var statearr_74051 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_74051[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_74051;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,xs,temp__4657__auto__))
);

return c__38109__auto__;
} else {
return null;
}
});
org.numenta.sanity.demos.cortical_io.set_model_BANG_ = (function org$numenta$sanity$demos$cortical_io$set_model_BANG_(){
return org.numenta.sanity.helpers.with_ui_loading_message((function (){
var n_regions = cljs.core.cst$kw$n_DASH_regions.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config)));
var spec = (function (){var G__74064 = (((cljs.core.cst$kw$spec_DASH_choice.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))) instanceof cljs.core.Keyword))?cljs.core.cst$kw$spec_DASH_choice.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))).fqn:null);
switch (G__74064) {
case "a":
return org.numenta.sanity.demos.cortical_io.spec_global;

break;
case "b":
return org.numenta.sanity.demos.cortical_io.spec_local;

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(cljs.core.cst$kw$spec_DASH_choice.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))))].join('')));

}
})();
var e = (function (){var G__74065 = (((cljs.core.cst$kw$encoder.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))) instanceof cljs.core.Keyword))?cljs.core.cst$kw$encoder.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))).fqn:null);
switch (G__74065) {
case "cortical-io":
return org.nfrac.comportex.cortical_io.cortical_io_encoder.cljs$core$IFn$_invoke$arity$variadic(cljs.core.cst$kw$api_DASH_key.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))),org.numenta.sanity.demos.cortical_io.fingerprint_cache,cljs.core.array_seq([cljs.core.cst$kw$decode_DASH_locally_QMARK_,cljs.core.cst$kw$decode_DASH_locally_QMARK_.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))),cljs.core.cst$kw$spatial_DASH_scramble_QMARK_,cljs.core.cst$kw$spatial_DASH_scramble_QMARK_.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config)))], 0));

break;
case "random":
return org.nfrac.comportex.encoders.unique_encoder(org.nfrac.comportex.cortical_io.retina_dim,cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core._STAR_,0.02,org.nfrac.comportex.cortical_io.retina_dim));

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(cljs.core.cst$kw$encoder.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.config))))].join('')));

}
})();
var sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$word,e], null);
var init_QMARK_ = ((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.model)) == null);
var G__74066_74072 = org.numenta.sanity.demos.cortical_io.model;
var G__74067_74073 = org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$4(n_regions,org.nfrac.comportex.core.sensory_region,cljs.core.list_STAR_.cljs$core$IFn$_invoke$arity$2(spec,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([spec,org.numenta.sanity.demos.cortical_io.higher_level_spec_diff], 0)))),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,sensor], null));
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__74066_74072,G__74067_74073) : cljs.core.reset_BANG_.call(null,G__74066_74072,G__74067_74073));

if(init_QMARK_){
org.numenta.sanity.bridge.browser.init.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.cortical_io.model,org.numenta.sanity.demos.cortical_io.world_c,org.numenta.sanity.main.into_journal,org.numenta.sanity.demos.cortical_io.into_sim);
} else {
var G__74068_74074 = org.numenta.sanity.main.network_shape;
var G__74069_74075 = org.numenta.sanity.util.translate_network_shape(org.numenta.sanity.comportex.data.network_shape((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.cortical_io.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.cortical_io.model))));
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__74068_74074,G__74069_74075) : cljs.core.reset_BANG_.call(null,G__74068_74074,G__74069_74075));
}

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.cortical_io.config,cljs.core.assoc,cljs.core.cst$kw$have_DASH_model_QMARK_,true);
}));
});
org.numenta.sanity.demos.cortical_io.config_template = new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"Input ",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Word sequences"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_info,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$label,cljs.core.cst$kw$id,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.cst$kw$postamble," queued input values."], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_info,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$label,cljs.core.cst$kw$id,cljs.core.cst$kw$cache_DASH_count,cljs.core.cst$kw$postamble," cached word fingerprints."], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Repeats of each sentence:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$repeats], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_12,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$textarea$form_DASH_control,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$textarea,cljs.core.cst$kw$id,cljs.core.cst$kw$text,cljs.core.cst$kw$rows,(10)], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_8,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$container,cljs.core.cst$kw$visible_QMARK_,(function (p1__74076_SHARP_){
return cljs.core.cst$kw$have_DASH_model_QMARK_.cljs$core$IFn$_invoke$arity$1(p1__74076_SHARP_);
})], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_primary,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.cortical_io.send_text_BANG_();

return e.preventDefault();
})], null),"Send text block input"], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$container,cljs.core.cst$kw$visible_QMARK_,(function (p1__74077_SHARP_){
return cljs.core.not(cljs.core.cst$kw$have_DASH_model_QMARK_.cljs$core$IFn$_invoke$arity$1(p1__74077_SHARP_));
})], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_primary$disabled,"Send text block input"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_info,"Create a model first (below)."], null)], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"HTM model"], null),new cljs.core.PersistentVector(null, 8, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Word encoder:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$select$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$list,cljs.core.cst$kw$id,cljs.core.cst$kw$encoder], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$option,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,cljs.core.cst$kw$cortical_DASH_io], null),"cortical.io"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$option,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,cljs.core.cst$kw$random], null),"random"], null)], null)], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$container,cljs.core.cst$kw$visible_QMARK_,(function (p1__74078_SHARP_){
return cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$cortical_DASH_io,cljs.core.cst$kw$encoder.cljs$core$IFn$_invoke$arity$1(p1__74078_SHARP_));
})], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Cortical.io API key:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$text,cljs.core.cst$kw$id,cljs.core.cst$kw$api_DASH_key], null)], null)], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Decode locally?"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$checkbox,cljs.core.cst$kw$id,cljs.core.cst$kw$decode_DASH_locally_QMARK_], null)], null)], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Spatial scramble?"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$checkbox,cljs.core.cst$kw$id,cljs.core.cst$kw$spatial_DASH_scramble_QMARK_], null)], null)], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Starting parameter set:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$select$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$list,cljs.core.cst$kw$id,cljs.core.cst$kw$spec_DASH_choice], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$option,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,cljs.core.cst$kw$a], null),"20% potential, no topology"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$option,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,cljs.core.cst$kw$b], null),"30% * local 16% area = 5% potential"], null)], null)], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Number of regions:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$n_DASH_regions], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_offset_DASH_5$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_primary,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.cortical_io.set_model_BANG_();

return e.preventDefault();
})], null),"Restart with new model"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_danger,"This resets all parameters."], null)], null)], null)], null)], null);
org.numenta.sanity.demos.cortical_io.model_tab = (function org$numenta$sanity$demos$cortical_io$model_tab(){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"This demo looks up the ",new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$a,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$href,"http://cortical.io/"], null),"cortical.io"], null)," fingerprint for each word. Enter your API key below to start. The\n     pre-loaded text below is the famous ",new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$a,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$href,"https://github.com/numenta/nupic.nlp-examples/blob/master/resources/associations/foxeat.csv"], null),"'fox eats what?' example"], null)," but you can enter whatever text you like. Words that are not\n      found in the cortical.io 'associative_en' retina are assigned a\n      random SDR."], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.bind_fields,org.numenta.sanity.demos.cortical_io.config_template,org.numenta.sanity.demos.cortical_io.config], null)], null);
});
org.numenta.sanity.demos.cortical_io.init = (function org$numenta$sanity$demos$cortical_io$init(){
reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,"Comportex",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.cortical_io.model_tab], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.cortical_io.world_pane], null),reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$model),org.numenta.sanity.demos.comportex_common.all_features,org.numenta.sanity.demos.cortical_io.into_sim], null),goog.dom.getElement("sanity-app"));

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.main.viz_options,cljs.core.assoc_in,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$drawing,cljs.core.cst$kw$display_DASH_mode], null),cljs.core.cst$kw$two_DASH_d);

return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.cortical_io.into_sim,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, ["run"], null));
});
goog.exportSymbol('org.numenta.sanity.demos.cortical_io.init', org.numenta.sanity.demos.cortical_io.init);
