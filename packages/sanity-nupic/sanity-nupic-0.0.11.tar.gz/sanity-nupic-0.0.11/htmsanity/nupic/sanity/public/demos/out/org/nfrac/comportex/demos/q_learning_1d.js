// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.demos.q_learning_1d');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.cells');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.synapses');
goog.require('org.nfrac.comportex.core');
goog.require('cljs.core.async');
goog.require('org.nfrac.comportex.util');
goog.require('org.nfrac.comportex.encoders');
org.nfrac.comportex.demos.q_learning_1d.input_dim = new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(400)], null);
org.nfrac.comportex.demos.q_learning_1d.n_on_bits = (40);
org.nfrac.comportex.demos.q_learning_1d.coord_radius = (60);
org.nfrac.comportex.demos.q_learning_1d.surface_coord_scale = (60);
org.nfrac.comportex.demos.q_learning_1d.surface = cljs.core.PersistentVector.fromArray([(0),0.5,(1),1.5,(2),1.5,(1),0.5,(0),(1),(2),(3),(4),(5),(4),(3),(2),(1),(1),(1),(1),(1),(1),(1),(2),(3),(4),(5),(6),(7),(8),(6),(4),(2)], true);
org.nfrac.comportex.demos.q_learning_1d.initial_inval = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(5),cljs.core.cst$kw$y,(org.nfrac.comportex.demos.q_learning_1d.surface.cljs$core$IFn$_invoke$arity$1 ? org.nfrac.comportex.demos.q_learning_1d.surface.cljs$core$IFn$_invoke$arity$1((5)) : org.nfrac.comportex.demos.q_learning_1d.surface.call(null,(5))),cljs.core.cst$kw$dy,(0),cljs.core.cst$kw$action,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$dx,(0)], null)], null);
org.nfrac.comportex.demos.q_learning_1d.spec = new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1000)], null),cljs.core.cst$kw$depth,(4),cljs.core.cst$kw$distal,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$punish_QMARK_,true], null),cljs.core.cst$kw$duty_DASH_cycle_DASH_period,(300),cljs.core.cst$kw$boost_DASH_active_DASH_duty_DASH_ratio,0.01,cljs.core.cst$kw$ff_DASH_potential_DASH_radius,0.15,cljs.core.cst$kw$ff_DASH_init_DASH_frac,0.5], null);
org.nfrac.comportex.demos.q_learning_1d.action_spec = cljs.core.PersistentHashMap.fromArrays([cljs.core.cst$kw$ff_DASH_perm_DASH_init_DASH_hi,cljs.core.cst$kw$q_DASH_alpha,cljs.core.cst$kw$freeze_QMARK_,cljs.core.cst$kw$ff_DASH_perm_DASH_init_DASH_lo,cljs.core.cst$kw$boost_DASH_active_DASH_duty_DASH_ratio,cljs.core.cst$kw$temporal_DASH_pooling_DASH_max_DASH_exc,cljs.core.cst$kw$column_DASH_dimensions,cljs.core.cst$kw$ff_DASH_init_DASH_frac,cljs.core.cst$kw$q_DASH_discount,cljs.core.cst$kw$boost_DASH_active_DASH_every,cljs.core.cst$kw$max_DASH_boost,cljs.core.cst$kw$ff_DASH_potential_DASH_radius,cljs.core.cst$kw$activation_DASH_level,cljs.core.cst$kw$proximal,cljs.core.cst$kw$depth,cljs.core.cst$kw$duty_DASH_cycle_DASH_period],[0.45,0.2,true,0.35,0.05,0.0,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(30)], null),0.5,0.8,(1),3.0,1.0,0.2,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$perm_DASH_inc,0.05,cljs.core.cst$kw$perm_DASH_dec,0.05,cljs.core.cst$kw$perm_DASH_connected,0.1], null),(1),(150)]);
org.nfrac.comportex.demos.q_learning_1d.direction__GT_action = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$left,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$dx,(-1)], null),cljs.core.cst$kw$right,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$dx,(1)], null)], null);
org.nfrac.comportex.demos.q_learning_1d.column__GT_signal = cljs.core.zipmap(cljs.core.range.cljs$core$IFn$_invoke$arity$0(),(function (){var iter__6925__auto__ = (function org$nfrac$comportex$demos$q_learning_1d$iter__71694(s__71695){
return (new cljs.core.LazySeq(null,(function (){
var s__71695__$1 = s__71695;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__71695__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var direction = cljs.core.first(xs__5205__auto__);
var iterys__6921__auto__ = ((function (s__71695__$1,direction,xs__5205__auto__,temp__4657__auto__){
return (function org$nfrac$comportex$demos$q_learning_1d$iter__71694_$_iter__71696(s__71697){
return (new cljs.core.LazySeq(null,((function (s__71695__$1,direction,xs__5205__auto__,temp__4657__auto__){
return (function (){
var s__71697__$1 = s__71697;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__71697__$1);
if(temp__4657__auto____$1){
var s__71697__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__71697__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71697__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71699 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71698 = (0);
while(true){
if((i__71698 < size__6924__auto__)){
var influence = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71698);
cljs.core.chunk_append(b__71699,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [direction,influence], null));

var G__71705 = (i__71698 + (1));
i__71698 = G__71705;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71699),org$nfrac$comportex$demos$q_learning_1d$iter__71694_$_iter__71696(cljs.core.chunk_rest(s__71697__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71699),null);
}
} else {
var influence = cljs.core.first(s__71697__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [direction,influence], null),org$nfrac$comportex$demos$q_learning_1d$iter__71694_$_iter__71696(cljs.core.rest(s__71697__$2)));
}
} else {
return null;
}
break;
}
});})(s__71695__$1,direction,xs__5205__auto__,temp__4657__auto__))
,null,null));
});})(s__71695__$1,direction,xs__5205__auto__,temp__4657__auto__))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.repeat.cljs$core$IFn$_invoke$arity$2((15),1.0)));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$nfrac$comportex$demos$q_learning_1d$iter__71694(cljs.core.rest(s__71695__$1)));
} else {
var G__71706 = cljs.core.rest(s__71695__$1);
s__71695__$1 = G__71706;
continue;
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$left,cljs.core.cst$kw$right], null));
})());
org.nfrac.comportex.demos.q_learning_1d.select_action = (function org$nfrac$comportex$demos$q_learning_1d$select_action(htm){
var alyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3], null));
var acols = org.nfrac.comportex.protocols.active_columns(alyr);
var signals = cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.demos.q_learning_1d.column__GT_signal,acols);
var G__71714 = cljs.core.key(cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core.max_key,cljs.core.val,cljs.core.shuffle(cljs.core.persistent_BANG_(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (alyr,acols,signals){
return (function (m,p__71715){
var vec__71716 = p__71715;
var motion = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71716,(0),null);
var influence = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71716,(1),null);
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(m,motion,(cljs.core.get.cljs$core$IFn$_invoke$arity$3(m,motion,(0)) + influence));
});})(alyr,acols,signals))
,cljs.core.transient$(cljs.core.PersistentArrayMap.EMPTY),signals)))));
return (org.nfrac.comportex.demos.q_learning_1d.direction__GT_action.cljs$core$IFn$_invoke$arity$1 ? org.nfrac.comportex.demos.q_learning_1d.direction__GT_action.cljs$core$IFn$_invoke$arity$1(G__71714) : org.nfrac.comportex.demos.q_learning_1d.direction__GT_action.call(null,G__71714));
});
org.nfrac.comportex.demos.q_learning_1d.apply_action = (function org$nfrac$comportex$demos$q_learning_1d$apply_action(inval){
var x = cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(inval);
var dx = cljs.core.cst$kw$dx.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval));
var next_x = (function (){var x__6484__auto__ = (function (){var x__6491__auto__ = (x + dx);
var y__6492__auto__ = (cljs.core.count(org.nfrac.comportex.demos.q_learning_1d.surface) - (1));
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})();
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var next_y = (org.nfrac.comportex.demos.q_learning_1d.surface.cljs$core$IFn$_invoke$arity$1 ? org.nfrac.comportex.demos.q_learning_1d.surface.cljs$core$IFn$_invoke$arity$1(next_x) : org.nfrac.comportex.demos.q_learning_1d.surface.call(null,next_x));
var dy = (next_y - cljs.core.cst$kw$y.cljs$core$IFn$_invoke$arity$1(inval));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(inval,cljs.core.cst$kw$x,next_x,cljs.core.array_seq([cljs.core.cst$kw$y,next_y,cljs.core.cst$kw$dy,dy], 0));
});
org.nfrac.comportex.demos.q_learning_1d.active_synapses = (function org$nfrac$comportex$demos$q_learning_1d$active_synapses(sg,target_id,ff_bits){
return cljs.core.filter.cljs$core$IFn$_invoke$arity$2((function (p__71719){
var vec__71720 = p__71719;
var in_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71720,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71720,(1),null);
return (ff_bits.cljs$core$IFn$_invoke$arity$1 ? ff_bits.cljs$core$IFn$_invoke$arity$1(in_id) : ff_bits.call(null,in_id));
}),org.nfrac.comportex.protocols.in_synapses(sg,target_id));
});
org.nfrac.comportex.demos.q_learning_1d.active_synapse_perms = (function org$nfrac$comportex$demos$q_learning_1d$active_synapse_perms(sg,target_id,ff_bits){
return cljs.core.keep.cljs$core$IFn$_invoke$arity$2((function (p__71723){
var vec__71724 = p__71723;
var in_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71724,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71724,(1),null);
if(cljs.core.truth_((ff_bits.cljs$core$IFn$_invoke$arity$1 ? ff_bits.cljs$core$IFn$_invoke$arity$1(in_id) : ff_bits.call(null,in_id)))){
return p;
} else {
return null;
}
}),org.nfrac.comportex.protocols.in_synapses(sg,target_id));
});
org.nfrac.comportex.demos.q_learning_1d.mean = (function org$nfrac$comportex$demos$q_learning_1d$mean(xs){
return (cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core._PLUS_,xs) / cljs.core.count(xs));
});
org.nfrac.comportex.demos.q_learning_1d.q_learn = (function org$nfrac$comportex$demos$q_learning_1d$q_learn(htm,prev_htm,reward){
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3], null),(function (lyr){
var prev_lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(prev_htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3], null));
var map__71727 = org.nfrac.comportex.protocols.params(lyr);
var map__71727__$1 = ((((!((map__71727 == null)))?((((map__71727.cljs$lang$protocol_mask$partition0$ & (64))) || (map__71727.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__71727):map__71727);
var ff_perm_init_lo = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__71727__$1,cljs.core.cst$kw$ff_DASH_perm_DASH_init_DASH_lo);
var q_alpha = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__71727__$1,cljs.core.cst$kw$q_DASH_alpha);
var q_discount = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__71727__$1,cljs.core.cst$kw$q_DASH_discount);
var ff_bits = (function (){var or__6153__auto__ = cljs.core.cst$kw$in_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.PersistentHashSet.EMPTY;
}
})();
var acols = cljs.core.cst$kw$active_DASH_cols.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr));
var prev_ff_bits = (function (){var or__6153__auto__ = cljs.core.cst$kw$in_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(prev_lyr));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.PersistentHashSet.EMPTY;
}
})();
var prev_acols = cljs.core.cst$kw$active_DASH_cols.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(prev_lyr));
var psg = cljs.core.cst$kw$proximal_DASH_sg.cljs$core$IFn$_invoke$arity$1(lyr);
var aperms = cljs.core.mapcat.cljs$core$IFn$_invoke$arity$variadic(((function (prev_lyr,map__71727,map__71727__$1,ff_perm_init_lo,q_alpha,q_discount,ff_bits,acols,prev_ff_bits,prev_acols,psg){
return (function (col){
return org.nfrac.comportex.demos.q_learning_1d.active_synapse_perms(psg,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0),(0)], null),ff_bits);
});})(prev_lyr,map__71727,map__71727__$1,ff_perm_init_lo,q_alpha,q_discount,ff_bits,acols,prev_ff_bits,prev_acols,psg))
,cljs.core.array_seq([acols], 0));
var Q_est = ((cljs.core.seq(aperms))?(org.nfrac.comportex.demos.q_learning_1d.mean(aperms) - ff_perm_init_lo):(0));
var Q_old = cljs.core.cst$kw$Q_DASH_val.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$Q_DASH_info.cljs$core$IFn$_invoke$arity$1(lyr),(0));
var learn_value = (reward + (q_discount * Q_est));
var adjust = (q_alpha * (learn_value - Q_old));
var op = (((adjust > (0)))?cljs.core.cst$kw$reinforce:cljs.core.cst$kw$punish);
var seg_updates = cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (prev_lyr,map__71727,map__71727__$1,ff_perm_init_lo,q_alpha,q_discount,ff_bits,acols,prev_ff_bits,prev_acols,psg,aperms,Q_est,Q_old,learn_value,adjust,op){
return (function (col){
return org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$4(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0),(0)], null),op,null,null);
});})(prev_lyr,map__71727,map__71727__$1,ff_perm_init_lo,q_alpha,q_discount,ff_bits,acols,prev_ff_bits,prev_acols,psg,aperms,Q_est,Q_old,learn_value,adjust,op))
,prev_acols);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(org.nfrac.comportex.protocols.layer_learn(lyr),cljs.core.cst$kw$proximal_DASH_sg,org.nfrac.comportex.protocols.bulk_learn(psg,seg_updates,prev_ff_bits,org.nfrac.comportex.util.abs(adjust),org.nfrac.comportex.util.abs(adjust),0.0)),cljs.core.cst$kw$Q_DASH_info,new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$Q_DASH_val,Q_est,cljs.core.cst$kw$Q_DASH_old,Q_old,cljs.core.cst$kw$reward,reward,cljs.core.cst$kw$lrn,learn_value,cljs.core.cst$kw$adj,adjust,cljs.core.cst$kw$perms,cljs.core.count(aperms)], null));
}));
});
org.nfrac.comportex.demos.q_learning_1d.make_model = (function org$nfrac$comportex$demos$q_learning_1d$make_model(){
var sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.encoders.vec_selector.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.cst$kw$x], 0)),org.nfrac.comportex.encoders.coordinate_encoder(org.nfrac.comportex.demos.q_learning_1d.input_dim,org.nfrac.comportex.demos.q_learning_1d.n_on_bits,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.q_learning_1d.surface_coord_scale], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.q_learning_1d.coord_radius], null))], null);
var msensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$action,cljs.core.cst$kw$dx], null),org.nfrac.comportex.encoders.linear_encoder.cljs$core$IFn$_invoke$arity$3(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(100)], null),(30),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(-1),(1)], null))], null);
return org.nfrac.comportex.core.region_network(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$rgn_DASH_1,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,cljs.core.cst$kw$motor], null),cljs.core.cst$kw$action,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rgn_DASH_1], null)], null),cljs.core.constantly(org.nfrac.comportex.core.sensory_region),new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$rgn_DASH_1,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(org.nfrac.comportex.demos.q_learning_1d.spec,cljs.core.cst$kw$lateral_DASH_synapses_QMARK_,false),cljs.core.cst$kw$action,org.nfrac.comportex.demos.q_learning_1d.action_spec], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,sensor], null),new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$input,sensor,cljs.core.cst$kw$motor,msensor], null));
});
org.nfrac.comportex.demos.q_learning_1d.htm_step_with_action_selection = (function org$nfrac$comportex$demos$q_learning_1d$htm_step_with_action_selection(world_c){
return (function (htm,inval){
var htm_a = org.nfrac.comportex.protocols.htm_learn(org.nfrac.comportex.protocols.htm_activate(org.nfrac.comportex.protocols.htm_sense(htm,inval,cljs.core.cst$kw$sensory)));
var reward = (0.5 * cljs.core.cst$kw$dy.cljs$core$IFn$_invoke$arity$1(inval));
var upd_htm = org.nfrac.comportex.demos.q_learning_1d.q_learn(htm_a,htm,reward);
var info = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(upd_htm,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3,cljs.core.cst$kw$Q_DASH_info], null));
var newQ = (function (){var x__6491__auto__ = (function (){var x__6484__auto__ = (cljs.core.cst$kw$Q_DASH_old.cljs$core$IFn$_invoke$arity$2(info,(0)) + cljs.core.cst$kw$adj.cljs$core$IFn$_invoke$arity$2(info,(0)));
var y__6485__auto__ = -1.0;
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var y__6492__auto__ = 1.0;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})();
var Q_map = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.cst$kw$Q_DASH_map.cljs$core$IFn$_invoke$arity$1(inval),cljs.core.select_keys(inval,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$x,cljs.core.cst$kw$action], null)),newQ);
var action = org.nfrac.comportex.demos.q_learning_1d.select_action(upd_htm);
var inval_with_action = cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(inval,cljs.core.cst$kw$action,action,cljs.core.array_seq([cljs.core.cst$kw$prev_DASH_action,cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval),cljs.core.cst$kw$Q_DASH_map,Q_map], 0));
var new_inval_71729 = org.nfrac.comportex.demos.q_learning_1d.apply_action(inval_with_action);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(world_c,new_inval_71729);

return org.nfrac.comportex.protocols.htm_depolarise(org.nfrac.comportex.protocols.htm_sense(upd_htm,inval_with_action,cljs.core.cst$kw$motor));
});
});
