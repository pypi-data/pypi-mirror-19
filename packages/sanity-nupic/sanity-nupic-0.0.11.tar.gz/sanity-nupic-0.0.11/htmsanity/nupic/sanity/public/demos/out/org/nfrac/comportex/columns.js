// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.columns');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.synapses');
goog.require('org.nfrac.comportex.topology');
goog.require('clojure.test.check.random');
goog.require('org.nfrac.comportex.util');
goog.require('org.nfrac.comportex.inhibition');
/**
 * Generates feed-forward synapses connecting columns to the input bit
 * array.
 * 
 * Connections are made locally by scaling the input space to the
 * column space. Potential synapses are chosen within a radius in
 * input space of `ff-potential-radius` fraction of the longest single
 * dimension, and of those, `ff-init-frac` are chosen from a
 * uniform random distribution.
 * 
 * Initial permanence values are uniformly distributed between
 * `ff-perm-init-lo` and `ff-perm-init-hi`.
 */
org.nfrac.comportex.columns.uniform_ff_synapses = (function org$nfrac$comportex$columns$uniform_ff_synapses(topo,itopo,spec,rng){
var p_hi = cljs.core.cst$kw$ff_DASH_perm_DASH_init_DASH_hi.cljs$core$IFn$_invoke$arity$1(spec);
var p_lo = cljs.core.cst$kw$ff_DASH_perm_DASH_init_DASH_lo.cljs$core$IFn$_invoke$arity$1(spec);
var global_QMARK_ = (cljs.core.cst$kw$ff_DASH_potential_DASH_radius.cljs$core$IFn$_invoke$arity$1(spec) >= 1.0);
var radius = cljs.core.long$((cljs.core.cst$kw$ff_DASH_potential_DASH_radius.cljs$core$IFn$_invoke$arity$1(spec) * cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.max,org.nfrac.comportex.protocols.dimensions(itopo))));
var frac = cljs.core.cst$kw$ff_DASH_init_DASH_frac.cljs$core$IFn$_invoke$arity$1(spec);
var input_size = org.nfrac.comportex.protocols.size(itopo);
var n_cols = org.nfrac.comportex.protocols.size(topo);
var one_d_QMARK_ = (((1) === cljs.core.count(org.nfrac.comportex.protocols.dimensions(topo)))) || (((1) === cljs.core.count(org.nfrac.comportex.protocols.dimensions(itopo))));
var vec__36607 = org.nfrac.comportex.protocols.dimensions(topo);
var cw = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36607,(0),null);
var ch = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36607,(1),null);
var cdepth = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36607,(2),null);
var vec__36608 = org.nfrac.comportex.protocols.dimensions(itopo);
var iw = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36608,(0),null);
var ih = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36608,(1),null);
var idepth = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36608,(2),null);
var focus_ix = ((function (p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth){
return (function (frac__$1,width){
return org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1(((frac__$1 * (width - ((2) * radius))) + radius));
});})(p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth))
;
var focus_izs = (cljs.core.truth_(idepth)?(((idepth <= (((2) * radius) + (1))))?cljs.core._conj(cljs.core.List.EMPTY,cljs.core.quot(idepth,(2))):cljs.core.range.cljs$core$IFn$_invoke$arity$2(radius,(idepth - radius))):null);
if(global_QMARK_){
var n_syns = org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((frac * input_size));
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (n_syns,p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs){
return (function (col_rng){
return cljs.core.into.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$1(((function (n_syns,p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs){
return (function (rng__$1){
var vec__36609 = clojure.test.check.random.split(rng__$1);
var rng1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36609,(0),null);
var rng2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36609,(1),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.util.rand_int.cljs$core$IFn$_invoke$arity$2(rng1,input_size),org.nfrac.comportex.util.rand(rng2,p_lo,p_hi)], null);
});})(n_syns,p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs))
),clojure.test.check.random.split_n(col_rng,n_syns));
});})(n_syns,p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs))
,clojure.test.check.random.split_n(rng,n_cols));
} else {
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$3(((function (p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs){
return (function (col,col_rng){
var focus_i = ((one_d_QMARK_)?org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((input_size * (col / n_cols))):(function (){var vec__36611 = org.nfrac.comportex.protocols.coordinates_of_index(topo,col);
var cx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36611,(0),null);
var cy = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36611,(1),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36611,(2),null);
var ix = focus_ix((cx / cw),iw);
var iy = focus_ix((cy / ch),ih);
var iz = (cljs.core.truth_(idepth)?cljs.core.nth.cljs$core$IFn$_invoke$arity$2(focus_izs,cljs.core.mod(col,cljs.core.count(focus_izs))):null);
var icoord = (cljs.core.truth_(idepth)?new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [ix,iy,iz], null):new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [ix,iy], null));
return org.nfrac.comportex.protocols.index_of_coordinates(itopo,icoord);
})());
var all_ids = cljs.core.vec(org.nfrac.comportex.protocols.neighbours_indices.cljs$core$IFn$_invoke$arity$4(itopo,focus_i,radius,(-1)));
var n = org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((frac * cljs.core.count(all_ids)));
var vec__36610 = clojure.test.check.random.split(col_rng);
var rng1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36610,(0),null);
var rng2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36610,(1),null);
var ids = (((frac < 0.4))?org.nfrac.comportex.util.sample(rng1,n,all_ids):(((frac < 1.0))?org.nfrac.comportex.util.reservoir_sample(rng1,n,all_ids):all_ids
));
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$3(((function (focus_i,all_ids,n,vec__36610,rng1,rng2,ids,p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs){
return (function (id,rng__$1){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [id,org.nfrac.comportex.util.rand(rng__$1,p_lo,p_hi)], null);
});})(focus_i,all_ids,n,vec__36610,rng1,rng2,ids,p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs))
,ids,clojure.test.check.random.split_n(rng2,cljs.core.count(ids))));
});})(p_hi,p_lo,global_QMARK_,radius,frac,input_size,n_cols,one_d_QMARK_,vec__36607,cw,ch,cdepth,vec__36608,iw,ih,idepth,focus_ix,focus_izs))
,cljs.core.range.cljs$core$IFn$_invoke$arity$0(),clojure.test.check.random.split_n(rng,n_cols));
}
});
/**
 * Given a map `exc` of the column overlap counts, multiplies the
 *   excitation value by the corresponding column boosting factor.
 */
org.nfrac.comportex.columns.apply_overlap_boosting = (function org$nfrac$comportex$columns$apply_overlap_boosting(exc,boosts){
return cljs.core.persistent_BANG_(cljs.core.reduce_kv((function (m,id,x){
var vec__36613 = id;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36613,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36613,(1),null);
var b = cljs.core.get.cljs$core$IFn$_invoke$arity$2(boosts,col);
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(m,id,(x * b));
}),cljs.core.transient$(cljs.core.PersistentArrayMap.EMPTY),exc));
});
org.nfrac.comportex.columns.ff_new_synapse_ids = (function org$nfrac$comportex$columns$ff_new_synapse_ids(rng,ff_bits,curr_ids_set,col,itopo,focus_coord,radius,n_grow){
var ids = cljs.core.List.EMPTY;
var on_bits = org.nfrac.comportex.util.shuffle(rng,ff_bits);
while(true){
if((cljs.core.empty_QMARK_(on_bits)) || ((cljs.core.count(ids) >= n_grow))){
return ids;
} else {
var id = cljs.core.first(ff_bits);
if(cljs.core.truth_((curr_ids_set.cljs$core$IFn$_invoke$arity$1 ? curr_ids_set.cljs$core$IFn$_invoke$arity$1(id) : curr_ids_set.call(null,id)))){
var G__36614 = ids;
var G__36615 = cljs.core.next(on_bits);
ids = G__36614;
on_bits = G__36615;
continue;
} else {
var coord = org.nfrac.comportex.protocols.coordinates_of_index(itopo,id);
var dist = org.nfrac.comportex.protocols.coord_distance(itopo,coord,focus_coord);
if((dist < radius)){
var G__36616 = cljs.core.conj.cljs$core$IFn$_invoke$arity$2(ids,id);
var G__36617 = cljs.core.next(on_bits);
ids = G__36616;
on_bits = G__36617;
continue;
} else {
var G__36618 = ids;
var G__36619 = cljs.core.next(on_bits);
ids = G__36618;
on_bits = G__36619;
continue;
}
}
}
break;
}
});
org.nfrac.comportex.columns.grow_new_synapses = (function org$nfrac$comportex$columns$grow_new_synapses(rng,ff_sg,col,ff_bits,itopo,radius,n_cols,n_grow,pinit){
var input_size = org.nfrac.comportex.protocols.size(itopo);
var focus_i = org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((input_size * (col / n_cols)));
var focus_coord = org.nfrac.comportex.protocols.coordinates_of_index(itopo,focus_i);
var new_ids = org.nfrac.comportex.columns.ff_new_synapse_ids(rng,ff_bits,org.nfrac.comportex.protocols.in_synapses(ff_sg,col),col,itopo,focus_coord,radius,n_grow);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,new_ids], null);
});
/**
 * y is the duty cycle value.
 */
org.nfrac.comportex.columns.boost_factor = (function org$nfrac$comportex$columns$boost_factor(y,neighbour_max,crit_ratio,max_boost){
var crit_y = (neighbour_max * crit_ratio);
var maxb = max_boost;
var x__6484__auto__ = (maxb - ((maxb - (1)) * (y / crit_y)));
var y__6485__auto__ = 1.0;
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
});
org.nfrac.comportex.columns.boost_factors_global = (function org$nfrac$comportex$columns$boost_factors_global(ys,spec){
var crit_ratio = cljs.core.cst$kw$boost_DASH_active_DASH_duty_DASH_ratio.cljs$core$IFn$_invoke$arity$1(spec);
var max_boost = cljs.core.cst$kw$max_DASH_boost.cljs$core$IFn$_invoke$arity$1(spec);
var max_y = cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core.max,(0),ys);
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (crit_ratio,max_boost,max_y){
return (function (y){
return org.nfrac.comportex.columns.boost_factor(y,max_y,crit_ratio,max_boost);
});})(crit_ratio,max_boost,max_y))
,ys);
});
org.nfrac.comportex.columns.boost_factors_local = (function org$nfrac$comportex$columns$boost_factors_local(ys,topo,inh_radius,spec){
var crit_ratio = cljs.core.cst$kw$boost_DASH_active_DASH_duty_DASH_ratio.cljs$core$IFn$_invoke$arity$1(spec);
var max_boost = cljs.core.cst$kw$max_DASH_boost.cljs$core$IFn$_invoke$arity$1(spec);
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$3(((function (crit_ratio,max_boost){
return (function (col,y){
var nb_is = org.nfrac.comportex.protocols.neighbours_indices.cljs$core$IFn$_invoke$arity$4(topo,col,inh_radius,(0));
var max_y = cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core.max,(0),cljs.core.map.cljs$core$IFn$_invoke$arity$2(ys,nb_is));
return org.nfrac.comportex.columns.boost_factor(y,max_y,crit_ratio,max_boost);
});})(crit_ratio,max_boost))
,cljs.core.range.cljs$core$IFn$_invoke$arity$0(),ys);
});
/**
 * Recalculates boost factors for each column based on its frequency
 * of activation (active duty cycle) compared to the maximum from its
 * neighbours.
 */
org.nfrac.comportex.columns.boost_active = (function org$nfrac$comportex$columns$boost_active(lyr){
if(!((cljs.core.cst$kw$boost_DASH_active_DASH_duty_DASH_ratio.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr)) > (0)))){
return lyr;
} else {
var global_QMARK_ = (cljs.core.cst$kw$ff_DASH_potential_DASH_radius.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr)) >= (1));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(lyr,cljs.core.cst$kw$boosts,((global_QMARK_)?org.nfrac.comportex.columns.boost_factors_global(cljs.core.cst$kw$active_DASH_duty_DASH_cycles.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr)):org.nfrac.comportex.columns.boost_factors_local(cljs.core.cst$kw$active_DASH_duty_DASH_cycles.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$topology.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$inh_DASH_radius.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr))));
}
});
org.nfrac.comportex.columns.adjust_overlap_global = (function org$nfrac$comportex$columns$adjust_overlap_global(sg,ys,spec){
var crit_ratio = cljs.core.cst$kw$adjust_DASH_overlap_DASH_duty_DASH_ratio.cljs$core$IFn$_invoke$arity$1(spec);
var max_y = cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core.max,(0),ys);
var crit_y = (max_y * crit_ratio);
var upds = cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (crit_ratio,max_y,crit_y){
return (function (p__36622){
var vec__36623 = p__36622;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36623,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36623,(1),null);
if((y <= crit_y)){
return org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$4(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0),(0)], null),cljs.core.cst$kw$reinforce,null,null);
} else {
return null;
}
});})(crit_ratio,max_y,crit_y))
,cljs.core.map.cljs$core$IFn$_invoke$arity$3(cljs.core.vector,cljs.core.range.cljs$core$IFn$_invoke$arity$0(),ys));
var pcon = cljs.core.cst$kw$perm_DASH_connected.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$proximal.cljs$core$IFn$_invoke$arity$1(spec));
return org.nfrac.comportex.protocols.bulk_learn(sg,upds,cljs.core.constantly(true),(0.1 * pcon),(0),(0));
});
org.nfrac.comportex.columns.adjust_overlap_local = (function org$nfrac$comportex$columns$adjust_overlap_local(sg,ys,topo,inh_radius,spec){
return org.nfrac.comportex.columns.adjust_overlap_global(sg,ys,spec);
});
org.nfrac.comportex.columns.adjust_overlap = (function org$nfrac$comportex$columns$adjust_overlap(lyr){
if(!((cljs.core.cst$kw$adjust_DASH_overlap_DASH_duty_DASH_ratio.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr)) > (0)))){
return lyr;
} else {
var global_QMARK_ = (cljs.core.cst$kw$ff_DASH_potential_DASH_radius.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr)) >= (1));
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(lyr,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$proximal_DASH_sg], null),((function (global_QMARK_){
return (function (sg){
if(global_QMARK_){
return org.nfrac.comportex.columns.adjust_overlap_global(sg,cljs.core.cst$kw$overlap_DASH_duty_DASH_cycles.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr));
} else {
return org.nfrac.comportex.columns.adjust_overlap_local(sg,cljs.core.cst$kw$overlap_DASH_duty_DASH_cycles.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$topology.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$inh_DASH_radius.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr));
}
});})(global_QMARK_))
);
}
});
org.nfrac.comportex.columns.float_overlap_global = (function org$nfrac$comportex$columns$float_overlap_global(sg,ys,spec){
var ref_y = cljs.core.cst$kw$activation_DASH_level.cljs$core$IFn$_invoke$arity$1(spec);
var lo_z = cljs.core.cst$kw$float_DASH_overlap_DASH_duty_DASH_ratio.cljs$core$IFn$_invoke$arity$1(spec);
var hi_z = cljs.core.cst$kw$float_DASH_overlap_DASH_duty_DASH_ratio_DASH_hi.cljs$core$IFn$_invoke$arity$1(spec);
var weaks = cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (ref_y,lo_z,hi_z){
return (function (p__36628){
var vec__36629 = p__36628;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36629,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36629,(1),null);
var z = (y / ref_y);
if((z < lo_z)){
return org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$4(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0),(0)], null),cljs.core.cst$kw$reinforce,null,null);
} else {
return null;
}
});})(ref_y,lo_z,hi_z))
,cljs.core.map.cljs$core$IFn$_invoke$arity$3(cljs.core.vector,cljs.core.range.cljs$core$IFn$_invoke$arity$0(),ys));
var strongs = cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (ref_y,lo_z,hi_z,weaks){
return (function (p__36630){
var vec__36631 = p__36630;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36631,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36631,(1),null);
var z = (y / ref_y);
if((z > hi_z)){
return org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$4(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0),(0)], null),cljs.core.cst$kw$punish,null,null);
} else {
return null;
}
});})(ref_y,lo_z,hi_z,weaks))
,cljs.core.map.cljs$core$IFn$_invoke$arity$3(cljs.core.vector,cljs.core.range.cljs$core$IFn$_invoke$arity$0(),ys));
var pcon = cljs.core.cst$kw$perm_DASH_connected.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$proximal.cljs$core$IFn$_invoke$arity$1(spec));
return org.nfrac.comportex.protocols.bulk_learn(sg,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(weaks,strongs),cljs.core.constantly(true),(0.1 * pcon),(0.1 * pcon),(0));
});
org.nfrac.comportex.columns.layer_float_overlap = (function org$nfrac$comportex$columns$layer_float_overlap(lyr){
if(!((cljs.core.cst$kw$float_DASH_overlap_DASH_duty_DASH_ratio.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr)) > (0)))){
return lyr;
} else {
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(lyr,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$proximal_DASH_sg], null),(function (sg){
return org.nfrac.comportex.columns.float_overlap_global(sg,cljs.core.cst$kw$active_DASH_duty_DASH_cycles.cljs$core$IFn$_invoke$arity$1(lyr),cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr));
}));
}
});
/**
 * Records a set of events with indices `is` in the vector `v`
 * according to duty cycle period `period`. As in NuPIC, the formula
 * is
 * 
 * <pre>
 * y[t] = (period-1) * y[t-1]  +  1
 *     --------------------------
 *       period
 * </pre>
 */
org.nfrac.comportex.columns.update_duty_cycles = (function org$nfrac$comportex$columns$update_duty_cycles(v,is,period){
var d = (1.0 / period);
var decay = (d * (period - (1)));
return org.nfrac.comportex.util.update_each(cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (d,decay){
return (function (p1__36632_SHARP_){
return (p1__36632_SHARP_ * decay);
});})(d,decay))
,v),is,((function (d,decay){
return (function (p1__36633_SHARP_){
return (p1__36633_SHARP_ + d);
});})(d,decay))
);
});
