// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.notebook');
goog.require('cljs.core');
goog.require('reagent.core');
goog.require('org.numenta.sanity.viz_canvas');
goog.require('org.numenta.sanity.demos.runner');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.numenta.sanity.bridge.remote');
goog.require('org.numenta.sanity.util');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('org.numenta.sanity.selection');
goog.require('cognitect.transit');
goog.require('org.nfrac.comportex.util');
goog.require('clojure.walk');
cljs.core.enable_console_print_BANG_();
org.numenta.sanity.demos.notebook.pipe_to_remote_target_BANG_ = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
org.numenta.sanity.demos.notebook.remote_target__GT_chan = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.PersistentArrayMap.EMPTY);
org.numenta.sanity.demos.notebook.connect = (function org$numenta$sanity$demos$notebook$connect(url){
var G__72307 = org.numenta.sanity.demos.notebook.pipe_to_remote_target_BANG_;
var G__72308 = org.numenta.sanity.bridge.remote.init(url);
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__72307,G__72308) : cljs.core.reset_BANG_.call(null,G__72307,G__72308));
});
goog.exportSymbol('org.numenta.sanity.demos.notebook.connect', org.numenta.sanity.demos.notebook.connect);
org.numenta.sanity.demos.notebook.read_transit_str = (function org$numenta$sanity$demos$notebook$read_transit_str(s){
return cognitect.transit.read(cognitect.transit.reader.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$json),s);
});
org.numenta.sanity.demos.notebook.display_inbits = (function org$numenta$sanity$demos$notebook$display_inbits(el,serialized){
var vec__72310 = org.numenta.sanity.demos.notebook.read_transit_str(serialized);
var dims = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72310,(0),null);
var state__GT_bits = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72310,(1),null);
var d_opts = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72310,(2),null);
return reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.viz_canvas.inbits_display,dims,state__GT_bits,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.cst$kw$drawing.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.viz_canvas.default_viz_options),d_opts], 0))], null),el);
});
goog.exportSymbol('org.numenta.sanity.demos.notebook.display_inbits', org.numenta.sanity.demos.notebook.display_inbits);
org.numenta.sanity.demos.notebook.release_inbits = (function org$numenta$sanity$demos$notebook$release_inbits(el){
return reagent.core.unmount_component_at_node(el);
});
goog.exportSymbol('org.numenta.sanity.demos.notebook.release_inbits', org.numenta.sanity.demos.notebook.release_inbits);
org.numenta.sanity.demos.notebook.add_viz = (function org$numenta$sanity$demos$notebook$add_viz(el,serialized){
var vec__72441 = org.numenta.sanity.demos.notebook.read_transit_str(serialized);
var journal_target = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72441,(0),null);
var opts = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72441,(1),null);
var into_journal = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var into_viz = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var response_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.notebook.remote_target__GT_chan,cljs.core.assoc,journal_target,into_journal);

(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.notebook.pipe_to_remote_target_BANG_) : cljs.core.deref.call(null,org.numenta.sanity.demos.notebook.pipe_to_remote_target_BANG_)).call(null,journal_target,into_journal);

cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(into_journal,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, ["get-network-shape",org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(response_c,true)], null));

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function (state_72549){
var state_val_72550 = (state_72549[(1)]);
if((state_val_72550 === (1))){
var state_72549__$1 = state_72549;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_72549__$1,(2),response_c);
} else {
if((state_val_72550 === (2))){
var inst_72446 = (state_72549[(7)]);
var inst_72443 = (state_72549[(2)]);
var inst_72444 = org.numenta.sanity.util.translate_network_shape(inst_72443);
var inst_72445 = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(inst_72444);
var inst_72446__$1 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var inst_72447 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72448 = org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(inst_72446__$1,true);
var inst_72449 = ["get-steps",inst_72448];
var inst_72450 = (new cljs.core.PersistentVector(null,2,(5),inst_72447,inst_72449,null));
var inst_72451 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(into_journal,inst_72450);
var state_72549__$1 = (function (){var statearr_72551 = state_72549;
(statearr_72551[(8)] = inst_72445);

(statearr_72551[(7)] = inst_72446__$1);

(statearr_72551[(9)] = inst_72451);

return statearr_72551;
})();
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_72549__$1,(3),inst_72446__$1);
} else {
if((state_val_72550 === (3))){
var inst_72445 = (state_72549[(8)]);
var inst_72460 = (state_72549[(10)]);
var inst_72446 = (state_72549[(7)]);
var inst_72454 = (state_72549[(11)]);
var inst_72454__$1 = (state_72549[(2)]);
var inst_72455 = (function (){var network_shape = inst_72445;
var response_c__$1 = inst_72446;
var all_steps = inst_72454__$1;
return ((function (network_shape,response_c__$1,all_steps,inst_72445,inst_72460,inst_72446,inst_72454,inst_72454__$1,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function (step){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(step,cljs.core.cst$kw$network_DASH_shape,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(network_shape) : cljs.core.deref.call(null,network_shape)));
});
;})(network_shape,response_c__$1,all_steps,inst_72445,inst_72460,inst_72446,inst_72454,inst_72454__$1,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
})();
var inst_72456 = clojure.walk.keywordize_keys(inst_72454__$1);
var inst_72457 = cljs.core.map.cljs$core$IFn$_invoke$arity$2(inst_72455,inst_72456);
var inst_72458 = cljs.core.reverse(inst_72457);
var inst_72459 = cljs.core.vec(inst_72458);
var inst_72460__$1 = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(inst_72459);
var inst_72461 = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.selection.blank_selection);
var inst_72463 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(inst_72460__$1) : cljs.core.deref.call(null,inst_72460__$1));
var inst_72464 = cljs.core.count(inst_72463);
var inst_72465 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((1),inst_72464);
var state_72549__$1 = (function (){var statearr_72552 = state_72549;
(statearr_72552[(10)] = inst_72460__$1);

(statearr_72552[(11)] = inst_72454__$1);

(statearr_72552[(12)] = inst_72461);

return statearr_72552;
})();
if(inst_72465){
var statearr_72553_72569 = state_72549__$1;
(statearr_72553_72569[(1)] = (4));

} else {
var statearr_72554_72570 = state_72549__$1;
(statearr_72554_72570[(1)] = (5));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_72550 === (4))){
var inst_72467 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72468 = [cljs.core.cst$kw$drawing,cljs.core.cst$kw$display_DASH_mode];
var inst_72469 = (new cljs.core.PersistentVector(null,2,(5),inst_72467,inst_72468,null));
var inst_72470 = cljs.core.assoc_in(org.numenta.sanity.viz_canvas.default_viz_options,inst_72469,cljs.core.cst$kw$two_DASH_d);
var state_72549__$1 = state_72549;
var statearr_72555_72571 = state_72549__$1;
(statearr_72555_72571[(2)] = inst_72470);

(statearr_72555_72571[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72550 === (5))){
var state_72549__$1 = state_72549;
var statearr_72556_72572 = state_72549__$1;
(statearr_72556_72572[(2)] = org.numenta.sanity.viz_canvas.default_viz_options);

(statearr_72556_72572[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72550 === (6))){
var inst_72445 = (state_72549[(8)]);
var inst_72460 = (state_72549[(10)]);
var inst_72446 = (state_72549[(7)]);
var inst_72454 = (state_72549[(11)]);
var inst_72476 = (state_72549[(13)]);
var inst_72461 = (state_72549[(12)]);
var inst_72473 = (state_72549[(2)]);
var inst_72474 = (function (){var network_shape = inst_72445;
var response_c__$1 = inst_72446;
var all_steps = inst_72454;
var steps = inst_72460;
var selection = inst_72461;
var base_opts = inst_72473;
return ((function (network_shape,response_c__$1,all_steps,steps,selection,base_opts,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function() { 
var G__72573__delegate = function (xs){
var last_non_nil = cljs.core.first(cljs.core.filter.cljs$core$IFn$_invoke$arity$2(cljs.core.complement(cljs.core.nil_QMARK_),cljs.core.reverse(xs)));
if(cljs.core.coll_QMARK_(last_non_nil)){
return last_non_nil;
} else {
return cljs.core.last(xs);
}
};
var G__72573 = function (var_args){
var xs = null;
if (arguments.length > 0) {
var G__72574__i = 0, G__72574__a = new Array(arguments.length -  0);
while (G__72574__i < G__72574__a.length) {G__72574__a[G__72574__i] = arguments[G__72574__i + 0]; ++G__72574__i;}
  xs = new cljs.core.IndexedSeq(G__72574__a,0);
} 
return G__72573__delegate.call(this,xs);};
G__72573.cljs$lang$maxFixedArity = 0;
G__72573.cljs$lang$applyTo = (function (arglist__72575){
var xs = cljs.core.seq(arglist__72575);
return G__72573__delegate(xs);
});
G__72573.cljs$core$IFn$_invoke$arity$variadic = G__72573__delegate;
return G__72573;
})()
;
;})(network_shape,response_c__$1,all_steps,steps,selection,base_opts,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
})();
var inst_72475 = org.nfrac.comportex.util.deep_merge_with.cljs$core$IFn$_invoke$arity$variadic(inst_72474,cljs.core.array_seq([inst_72473,opts], 0));
var inst_72476__$1 = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(inst_72475);
var inst_72477 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(inst_72445) : cljs.core.deref.call(null,inst_72445));
var inst_72478 = cljs.core.cst$kw$regions.cljs$core$IFn$_invoke$arity$1(inst_72477);
var inst_72479 = cljs.core.seq(inst_72478);
var inst_72480 = cljs.core.first(inst_72479);
var inst_72481 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_72480,(0),null);
var inst_72482 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_72480,(1),null);
var inst_72483 = cljs.core.keys(inst_72482);
var inst_72484 = cljs.core.first(inst_72483);
var inst_72486 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(inst_72445) : cljs.core.deref.call(null,inst_72445));
var inst_72487 = cljs.core.cst$kw$regions.cljs$core$IFn$_invoke$arity$1(inst_72486);
var inst_72488 = cljs.core.seq(inst_72487);
var inst_72489 = cljs.core.first(inst_72488);
var inst_72490 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_72489,(0),null);
var inst_72491 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_72489,(1),null);
var inst_72492 = cljs.core.keys(inst_72491);
var inst_72493 = cljs.core.first(inst_72492);
var inst_72494 = (function (){var selection = inst_72461;
var network_shape = inst_72445;
var base_opts = inst_72473;
var response_c__$1 = inst_72446;
var all_steps = inst_72454;
var steps = inst_72460;
var viz_options = inst_72476__$1;
var vec__72485 = inst_72489;
var vec__72452 = inst_72480;
var layer_id = inst_72493;
var rgn = inst_72491;
var region_key = inst_72490;
return ((function (selection,network_shape,base_opts,response_c__$1,all_steps,steps,viz_options,vec__72485,vec__72452,layer_id,rgn,region_key,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,inst_72474,inst_72475,inst_72476__$1,inst_72477,inst_72478,inst_72479,inst_72480,inst_72481,inst_72482,inst_72483,inst_72484,inst_72486,inst_72487,inst_72488,inst_72489,inst_72490,inst_72491,inst_72492,inst_72493,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function (p1__72311_SHARP_){
return cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cljs.core.empty(p1__72311_SHARP_),new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$dt,(0),cljs.core.cst$kw$region,region_key,cljs.core.cst$kw$layer,layer_id,cljs.core.cst$kw$snapshot_DASH_id,cljs.core.cst$kw$snapshot_DASH_id.cljs$core$IFn$_invoke$arity$1(cljs.core.first((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps) : cljs.core.deref.call(null,steps))))], null));
});
;})(selection,network_shape,base_opts,response_c__$1,all_steps,steps,viz_options,vec__72485,vec__72452,layer_id,rgn,region_key,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,inst_72474,inst_72475,inst_72476__$1,inst_72477,inst_72478,inst_72479,inst_72480,inst_72481,inst_72482,inst_72483,inst_72484,inst_72486,inst_72487,inst_72488,inst_72489,inst_72490,inst_72491,inst_72492,inst_72493,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
})();
var inst_72495 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(inst_72461,inst_72494);
var inst_72496 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72497 = [cljs.core.cst$kw$on_DASH_click,cljs.core.cst$kw$on_DASH_key_DASH_down,cljs.core.cst$kw$tabIndex];
var inst_72498 = (function (){var selection = inst_72461;
var network_shape = inst_72445;
var base_opts = inst_72473;
var response_c__$1 = inst_72446;
var all_steps = inst_72454;
var steps = inst_72460;
var viz_options = inst_72476__$1;
var vec__72452 = inst_72480;
var layer_id = inst_72484;
var rgn = inst_72482;
var region_key = inst_72481;
return ((function (selection,network_shape,base_opts,response_c__$1,all_steps,steps,viz_options,vec__72452,layer_id,rgn,region_key,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,inst_72474,inst_72475,inst_72476__$1,inst_72477,inst_72478,inst_72479,inst_72480,inst_72481,inst_72482,inst_72483,inst_72484,inst_72486,inst_72487,inst_72488,inst_72489,inst_72490,inst_72491,inst_72492,inst_72493,inst_72494,inst_72495,inst_72496,inst_72497,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function (){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(into_viz,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$background_DASH_clicked], null));
});
;})(selection,network_shape,base_opts,response_c__$1,all_steps,steps,viz_options,vec__72452,layer_id,rgn,region_key,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,inst_72474,inst_72475,inst_72476__$1,inst_72477,inst_72478,inst_72479,inst_72480,inst_72481,inst_72482,inst_72483,inst_72484,inst_72486,inst_72487,inst_72488,inst_72489,inst_72490,inst_72491,inst_72492,inst_72493,inst_72494,inst_72495,inst_72496,inst_72497,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
})();
var inst_72499 = (function (){var selection = inst_72461;
var network_shape = inst_72445;
var base_opts = inst_72473;
var response_c__$1 = inst_72446;
var all_steps = inst_72454;
var steps = inst_72460;
var viz_options = inst_72476__$1;
var vec__72452 = inst_72480;
var layer_id = inst_72484;
var rgn = inst_72482;
var region_key = inst_72481;
return ((function (selection,network_shape,base_opts,response_c__$1,all_steps,steps,viz_options,vec__72452,layer_id,rgn,region_key,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,inst_72474,inst_72475,inst_72476__$1,inst_72477,inst_72478,inst_72479,inst_72480,inst_72481,inst_72482,inst_72483,inst_72484,inst_72486,inst_72487,inst_72488,inst_72489,inst_72490,inst_72491,inst_72492,inst_72493,inst_72494,inst_72495,inst_72496,inst_72497,inst_72498,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function (p1__72312_SHARP_){
return org.numenta.sanity.viz_canvas.viz_key_down(p1__72312_SHARP_,into_viz);
});
;})(selection,network_shape,base_opts,response_c__$1,all_steps,steps,viz_options,vec__72452,layer_id,rgn,region_key,inst_72445,inst_72460,inst_72446,inst_72454,inst_72476,inst_72461,inst_72473,inst_72474,inst_72475,inst_72476__$1,inst_72477,inst_72478,inst_72479,inst_72480,inst_72481,inst_72482,inst_72483,inst_72484,inst_72486,inst_72487,inst_72488,inst_72489,inst_72490,inst_72491,inst_72492,inst_72493,inst_72494,inst_72495,inst_72496,inst_72497,inst_72498,state_val_72550,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
})();
var inst_72500 = [inst_72498,inst_72499,(1)];
var inst_72501 = cljs.core.PersistentHashMap.fromArrays(inst_72497,inst_72500);
var inst_72502 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(inst_72460) : cljs.core.deref.call(null,inst_72460));
var inst_72503 = cljs.core.count(inst_72502);
var inst_72504 = (inst_72503 > (1));
var state_72549__$1 = (function (){var statearr_72557 = state_72549;
(statearr_72557[(14)] = inst_72495);

(statearr_72557[(15)] = inst_72501);

(statearr_72557[(13)] = inst_72476__$1);

(statearr_72557[(16)] = inst_72496);

return statearr_72557;
})();
if(cljs.core.truth_(inst_72504)){
var statearr_72558_72576 = state_72549__$1;
(statearr_72558_72576[(1)] = (7));

} else {
var statearr_72559_72577 = state_72549__$1;
(statearr_72559_72577[(1)] = (8));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_72550 === (7))){
var inst_72460 = (state_72549[(10)]);
var inst_72476 = (state_72549[(13)]);
var inst_72461 = (state_72549[(12)]);
var inst_72506 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72507 = [org.numenta.sanity.viz_canvas.viz_timeline,inst_72460,inst_72461,inst_72476];
var inst_72508 = (new cljs.core.PersistentVector(null,4,(5),inst_72506,inst_72507,null));
var state_72549__$1 = state_72549;
var statearr_72560_72578 = state_72549__$1;
(statearr_72560_72578[(2)] = inst_72508);

(statearr_72560_72578[(1)] = (9));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72550 === (8))){
var state_72549__$1 = state_72549;
var statearr_72561_72579 = state_72549__$1;
(statearr_72561_72579[(2)] = null);

(statearr_72561_72579[(1)] = (9));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72550 === (9))){
var inst_72445 = (state_72549[(8)]);
var inst_72460 = (state_72549[(10)]);
var inst_72501 = (state_72549[(15)]);
var inst_72476 = (state_72549[(13)]);
var inst_72496 = (state_72549[(16)]);
var inst_72461 = (state_72549[(12)]);
var inst_72511 = (state_72549[(2)]);
var inst_72512 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72513 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72514 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72515 = [cljs.core.cst$kw$style];
var inst_72516 = [cljs.core.cst$kw$border,cljs.core.cst$kw$vertical_DASH_align];
var inst_72517 = ["none","top"];
var inst_72518 = cljs.core.PersistentHashMap.fromArrays(inst_72516,inst_72517);
var inst_72519 = [inst_72518];
var inst_72520 = cljs.core.PersistentHashMap.fromArrays(inst_72515,inst_72519);
var inst_72521 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72522 = [org.numenta.sanity.demos.runner.world_pane,inst_72460,inst_72461];
var inst_72523 = (new cljs.core.PersistentVector(null,3,(5),inst_72521,inst_72522,null));
var inst_72524 = [cljs.core.cst$kw$td,inst_72520,inst_72523];
var inst_72525 = (new cljs.core.PersistentVector(null,3,(5),inst_72514,inst_72524,null));
var inst_72526 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72527 = [cljs.core.cst$kw$style];
var inst_72528 = [cljs.core.cst$kw$border,cljs.core.cst$kw$vertical_DASH_align];
var inst_72529 = ["none","top"];
var inst_72530 = cljs.core.PersistentHashMap.fromArrays(inst_72528,inst_72529);
var inst_72531 = [inst_72530];
var inst_72532 = cljs.core.PersistentHashMap.fromArrays(inst_72527,inst_72531);
var inst_72533 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72534 = [cljs.core.cst$kw$tabIndex];
var inst_72535 = [(0)];
var inst_72536 = cljs.core.PersistentHashMap.fromArrays(inst_72534,inst_72535);
var inst_72537 = [org.numenta.sanity.viz_canvas.viz_canvas,inst_72536,inst_72460,inst_72461,inst_72445,inst_72476,into_viz,null,into_journal];
var inst_72538 = (new cljs.core.PersistentVector(null,9,(5),inst_72533,inst_72537,null));
var inst_72539 = [cljs.core.cst$kw$td,inst_72532,inst_72538];
var inst_72540 = (new cljs.core.PersistentVector(null,3,(5),inst_72526,inst_72539,null));
var inst_72541 = [cljs.core.cst$kw$tr,inst_72525,inst_72540];
var inst_72542 = (new cljs.core.PersistentVector(null,3,(5),inst_72513,inst_72541,null));
var inst_72543 = [cljs.core.cst$kw$table,inst_72542];
var inst_72544 = (new cljs.core.PersistentVector(null,2,(5),inst_72512,inst_72543,null));
var inst_72545 = [cljs.core.cst$kw$div,inst_72501,inst_72511,inst_72544];
var inst_72546 = (new cljs.core.PersistentVector(null,4,(5),inst_72496,inst_72545,null));
var inst_72547 = reagent.core.render.cljs$core$IFn$_invoke$arity$2(inst_72546,el);
var state_72549__$1 = state_72549;
return cljs.core.async.impl.ioc_helpers.return_chan(state_72549__$1,inst_72547);
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
});})(c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
;
return ((function (switch__37995__auto__,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c){
return (function() {
var org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto____0 = (function (){
var statearr_72565 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_72565[(0)] = org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto__);

(statearr_72565[(1)] = (1));

return statearr_72565;
});
var org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto____1 = (function (state_72549){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_72549);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e72566){if((e72566 instanceof Object)){
var ex__37999__auto__ = e72566;
var statearr_72567_72580 = state_72549;
(statearr_72567_72580[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_72549);

return cljs.core.cst$kw$recur;
} else {
throw e72566;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__72581 = state_72549;
state_72549 = G__72581;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto__ = function(state_72549){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto____1.call(this,state_72549);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$notebook$add_viz_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
})();
var state__38111__auto__ = (function (){var statearr_72568 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_72568[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_72568;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,vec__72441,journal_target,opts,into_journal,into_viz,response_c))
);

return c__38109__auto__;
});
goog.exportSymbol('org.numenta.sanity.demos.notebook.add_viz', org.numenta.sanity.demos.notebook.add_viz);
org.numenta.sanity.demos.notebook.release_viz = (function org$numenta$sanity$demos$notebook$release_viz(el,serialized){
reagent.core.unmount_component_at_node(el);

var journal_target = org.numenta.sanity.demos.notebook.read_transit_str(serialized);
cljs.core.async.close_BANG_(cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.notebook.remote_target__GT_chan) : cljs.core.deref.call(null,org.numenta.sanity.demos.notebook.remote_target__GT_chan)),journal_target));

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.demos.notebook.remote_target__GT_chan,cljs.core.dissoc,journal_target);
});
goog.exportSymbol('org.numenta.sanity.demos.notebook.release_viz', org.numenta.sanity.demos.notebook.release_viz);
org.numenta.sanity.demos.notebook.exported_viz = (function org$numenta$sanity$demos$notebook$exported_viz(el){
var cnvs = cljs.core.array_seq.cljs$core$IFn$_invoke$arity$1(el.getElementsByTagName("canvas"));
var copy_el = document.createElement("div");
copy_el.innerHTML = el.innerHTML;

var seq__72588_72594 = cljs.core.seq(cnvs);
var chunk__72590_72595 = null;
var count__72591_72596 = (0);
var i__72592_72597 = (0);
while(true){
if((i__72592_72597 < count__72591_72596)){
var cnv_72598 = chunk__72590_72595.cljs$core$IIndexed$_nth$arity$2(null,i__72592_72597);
var victim_el_72599 = (copy_el.getElementsByTagName("canvas")[(0)]);
var img_el_72600 = document.createElement("img");
img_el_72600.setAttribute("src",cnv_72598.toDataURL("image/png"));

var temp__4657__auto___72601 = victim_el_72599.getAttribute("style");
if(cljs.core.truth_(temp__4657__auto___72601)){
var style_72602 = temp__4657__auto___72601;
img_el_72600.setAttribute("style",style_72602);
} else {
}

victim_el_72599.parentNode.replaceChild(img_el_72600,victim_el_72599);

var G__72603 = seq__72588_72594;
var G__72604 = chunk__72590_72595;
var G__72605 = count__72591_72596;
var G__72606 = (i__72592_72597 + (1));
seq__72588_72594 = G__72603;
chunk__72590_72595 = G__72604;
count__72591_72596 = G__72605;
i__72592_72597 = G__72606;
continue;
} else {
var temp__4657__auto___72607 = cljs.core.seq(seq__72588_72594);
if(temp__4657__auto___72607){
var seq__72588_72608__$1 = temp__4657__auto___72607;
if(cljs.core.chunked_seq_QMARK_(seq__72588_72608__$1)){
var c__6956__auto___72609 = cljs.core.chunk_first(seq__72588_72608__$1);
var G__72610 = cljs.core.chunk_rest(seq__72588_72608__$1);
var G__72611 = c__6956__auto___72609;
var G__72612 = cljs.core.count(c__6956__auto___72609);
var G__72613 = (0);
seq__72588_72594 = G__72610;
chunk__72590_72595 = G__72611;
count__72591_72596 = G__72612;
i__72592_72597 = G__72613;
continue;
} else {
var cnv_72614 = cljs.core.first(seq__72588_72608__$1);
var victim_el_72615 = (copy_el.getElementsByTagName("canvas")[(0)]);
var img_el_72616 = document.createElement("img");
img_el_72616.setAttribute("src",cnv_72614.toDataURL("image/png"));

var temp__4657__auto___72617__$1 = victim_el_72615.getAttribute("style");
if(cljs.core.truth_(temp__4657__auto___72617__$1)){
var style_72618 = temp__4657__auto___72617__$1;
img_el_72616.setAttribute("style",style_72618);
} else {
}

victim_el_72615.parentNode.replaceChild(img_el_72616,victim_el_72615);

var G__72619 = cljs.core.next(seq__72588_72608__$1);
var G__72620 = null;
var G__72621 = (0);
var G__72622 = (0);
seq__72588_72594 = G__72619;
chunk__72590_72595 = G__72620;
count__72591_72596 = G__72621;
i__72592_72597 = G__72622;
continue;
}
} else {
}
}
break;
}

return copy_el.innerHTML;
});
goog.exportSymbol('org.numenta.sanity.demos.notebook.exported_viz', org.numenta.sanity.demos.notebook.exported_viz);
