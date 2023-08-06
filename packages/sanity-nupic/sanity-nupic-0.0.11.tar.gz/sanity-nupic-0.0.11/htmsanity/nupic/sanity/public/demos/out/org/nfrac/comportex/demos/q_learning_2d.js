// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.demos.q_learning_2d');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.cells');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.demos.q_learning_1d');
goog.require('cljs.core.async');
goog.require('org.nfrac.comportex.util');
goog.require('org.nfrac.comportex.encoders');
org.nfrac.comportex.demos.q_learning_2d.input_dim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(10),(40)], null);
org.nfrac.comportex.demos.q_learning_2d.grid_w = (7);
org.nfrac.comportex.demos.q_learning_2d.grid_h = (7);
org.nfrac.comportex.demos.q_learning_2d.n_on_bits = (40);
org.nfrac.comportex.demos.q_learning_2d.coord_radius = (5);
org.nfrac.comportex.demos.q_learning_2d.surface_coord_scale = (5);
org.nfrac.comportex.demos.q_learning_2d.empty_reward = (-3);
org.nfrac.comportex.demos.q_learning_2d.hazard_reward = (-200);
org.nfrac.comportex.demos.q_learning_2d.finish_reward = (200);
org.nfrac.comportex.demos.q_learning_2d.surface = cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(cljs.core.vec,(function (){var iter__6925__auto__ = (function org$nfrac$comportex$demos$q_learning_2d$iter__72800(s__72801){
return (new cljs.core.LazySeq(null,(function (){
var s__72801__$1 = s__72801;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__72801__$1);
if(temp__4657__auto__){
var s__72801__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__72801__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__72801__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__72803 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__72802 = (0);
while(true){
if((i__72802 < size__6924__auto__)){
var x = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__72802);
cljs.core.chunk_append(b__72803,(function (){var iter__6925__auto__ = ((function (i__72802,x,c__6923__auto__,size__6924__auto__,b__72803,s__72801__$2,temp__4657__auto__){
return (function org$nfrac$comportex$demos$q_learning_2d$iter__72800_$_iter__72826(s__72827){
return (new cljs.core.LazySeq(null,((function (i__72802,x,c__6923__auto__,size__6924__auto__,b__72803,s__72801__$2,temp__4657__auto__){
return (function (){
var s__72827__$1 = s__72827;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__72827__$1);
if(temp__4657__auto____$1){
var s__72827__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__72827__$2)){
var c__6923__auto____$1 = cljs.core.chunk_first(s__72827__$2);
var size__6924__auto____$1 = cljs.core.count(c__6923__auto____$1);
var b__72829 = cljs.core.chunk_buffer(size__6924__auto____$1);
if((function (){var i__72828 = (0);
while(true){
if((i__72828 < size__6924__auto____$1)){
var y = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$1,i__72828);
cljs.core.chunk_append(b__72829,(function (){var G__72834 = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y], null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(org.nfrac.comportex.demos.q_learning_2d.grid_h - (1))], null),G__72834)){
return org.nfrac.comportex.demos.q_learning_2d.finish_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)) - (2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72834)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72834)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2)) - (1))], null),G__72834)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(0)], null),G__72834)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
return org.nfrac.comportex.demos.q_learning_2d.empty_reward;

}
}
}
}
}
})());

var G__72846 = (i__72828 + (1));
i__72828 = G__72846;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__72829),org$nfrac$comportex$demos$q_learning_2d$iter__72800_$_iter__72826(cljs.core.chunk_rest(s__72827__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__72829),null);
}
} else {
var y = cljs.core.first(s__72827__$2);
return cljs.core.cons((function (){var G__72835 = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y], null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(org.nfrac.comportex.demos.q_learning_2d.grid_h - (1))], null),G__72835)){
return org.nfrac.comportex.demos.q_learning_2d.finish_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)) - (2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72835)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72835)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2)) - (1))], null),G__72835)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(0)], null),G__72835)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
return org.nfrac.comportex.demos.q_learning_2d.empty_reward;

}
}
}
}
}
})(),org$nfrac$comportex$demos$q_learning_2d$iter__72800_$_iter__72826(cljs.core.rest(s__72827__$2)));
}
} else {
return null;
}
break;
}
});})(i__72802,x,c__6923__auto__,size__6924__auto__,b__72803,s__72801__$2,temp__4657__auto__))
,null,null));
});})(i__72802,x,c__6923__auto__,size__6924__auto__,b__72803,s__72801__$2,temp__4657__auto__))
;
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.q_learning_2d.grid_h));
})());

var G__72847 = (i__72802 + (1));
i__72802 = G__72847;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__72803),org$nfrac$comportex$demos$q_learning_2d$iter__72800(cljs.core.chunk_rest(s__72801__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__72803),null);
}
} else {
var x = cljs.core.first(s__72801__$2);
return cljs.core.cons((function (){var iter__6925__auto__ = ((function (x,s__72801__$2,temp__4657__auto__){
return (function org$nfrac$comportex$demos$q_learning_2d$iter__72800_$_iter__72836(s__72837){
return (new cljs.core.LazySeq(null,((function (x,s__72801__$2,temp__4657__auto__){
return (function (){
var s__72837__$1 = s__72837;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__72837__$1);
if(temp__4657__auto____$1){
var s__72837__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__72837__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__72837__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__72839 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__72838 = (0);
while(true){
if((i__72838 < size__6924__auto__)){
var y = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__72838);
cljs.core.chunk_append(b__72839,(function (){var G__72844 = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y], null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(org.nfrac.comportex.demos.q_learning_2d.grid_h - (1))], null),G__72844)){
return org.nfrac.comportex.demos.q_learning_2d.finish_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)) - (2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72844)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72844)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2)) - (1))], null),G__72844)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(0)], null),G__72844)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
return org.nfrac.comportex.demos.q_learning_2d.empty_reward;

}
}
}
}
}
})());

var G__72848 = (i__72838 + (1));
i__72838 = G__72848;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__72839),org$nfrac$comportex$demos$q_learning_2d$iter__72800_$_iter__72836(cljs.core.chunk_rest(s__72837__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__72839),null);
}
} else {
var y = cljs.core.first(s__72837__$2);
return cljs.core.cons((function (){var G__72845 = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x,y], null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(org.nfrac.comportex.demos.q_learning_2d.grid_h - (1))], null),G__72845)){
return org.nfrac.comportex.demos.q_learning_2d.finish_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)) - (2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72845)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2))], null),G__72845)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_w,(2)),(cljs.core.quot(org.nfrac.comportex.demos.q_learning_2d.grid_h,(2)) - (1))], null),G__72845)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1)),(0)], null),G__72845)){
return org.nfrac.comportex.demos.q_learning_2d.hazard_reward;
} else {
return org.nfrac.comportex.demos.q_learning_2d.empty_reward;

}
}
}
}
}
})(),org$nfrac$comportex$demos$q_learning_2d$iter__72800_$_iter__72836(cljs.core.rest(s__72837__$2)));
}
} else {
return null;
}
break;
}
});})(x,s__72801__$2,temp__4657__auto__))
,null,null));
});})(x,s__72801__$2,temp__4657__auto__))
;
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.q_learning_2d.grid_h));
})(),org$nfrac$comportex$demos$q_learning_2d$iter__72800(cljs.core.rest(s__72801__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.q_learning_2d.grid_w));
})());
org.nfrac.comportex.demos.q_learning_2d.initial_inval = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$z,(0),cljs.core.cst$kw$action,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$dx,(0),cljs.core.cst$kw$dy,(0)], null)], null);
org.nfrac.comportex.demos.q_learning_2d.spec = new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(30),(30)], null),cljs.core.cst$kw$depth,(4),cljs.core.cst$kw$distal_DASH_punish_QMARK_,true,cljs.core.cst$kw$duty_DASH_cycle_DASH_period,(300),cljs.core.cst$kw$boost_DASH_active_DASH_duty_DASH_ratio,0.01,cljs.core.cst$kw$ff_DASH_potential_DASH_radius,0.15,cljs.core.cst$kw$ff_DASH_init_DASH_frac,0.5], null);
org.nfrac.comportex.demos.q_learning_2d.action_spec = cljs.core.PersistentHashMap.fromArrays([cljs.core.cst$kw$ff_DASH_perm_DASH_init_DASH_hi,cljs.core.cst$kw$q_DASH_alpha,cljs.core.cst$kw$freeze_QMARK_,cljs.core.cst$kw$ff_DASH_perm_DASH_init_DASH_lo,cljs.core.cst$kw$boost_DASH_active_DASH_duty_DASH_ratio,cljs.core.cst$kw$temporal_DASH_pooling_DASH_max_DASH_exc,cljs.core.cst$kw$column_DASH_dimensions,cljs.core.cst$kw$ff_DASH_init_DASH_frac,cljs.core.cst$kw$q_DASH_discount,cljs.core.cst$kw$boost_DASH_active_DASH_every,cljs.core.cst$kw$max_DASH_boost,cljs.core.cst$kw$ff_DASH_potential_DASH_radius,cljs.core.cst$kw$activation_DASH_level,cljs.core.cst$kw$proximal,cljs.core.cst$kw$depth,cljs.core.cst$kw$duty_DASH_cycle_DASH_period],[0.45,0.75,true,0.35,0.05,0.0,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(4),(10)], null),0.5,0.9,(1),3.0,(1),0.2,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$perm_DASH_inc,0.05,cljs.core.cst$kw$perm_DASH_dec,0.05,cljs.core.cst$kw$perm_DASH_connected,0.1], null),(1),(250)]);
org.nfrac.comportex.demos.q_learning_2d.direction__GT_action = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$up,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$dx,(0),cljs.core.cst$kw$dy,(-1)], null),cljs.core.cst$kw$down,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$dx,(0),cljs.core.cst$kw$dy,(1)], null),cljs.core.cst$kw$left,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$dx,(-1),cljs.core.cst$kw$dy,(0)], null),cljs.core.cst$kw$right,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$dx,(1),cljs.core.cst$kw$dy,(0)], null)], null);
org.nfrac.comportex.demos.q_learning_2d.possible_directions = (function org$nfrac$comportex$demos$q_learning_2d$possible_directions(p__72849){
var vec__72852 = p__72849;
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72852,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72852,(1),null);
var G__72853 = new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$down,null,cljs.core.cst$kw$up,null,cljs.core.cst$kw$right,null,cljs.core.cst$kw$left,null], null), null);
var G__72853__$1 = (((x === (0)))?cljs.core.disj.cljs$core$IFn$_invoke$arity$2(G__72853,cljs.core.cst$kw$left):G__72853);
var G__72853__$2 = (((y === (0)))?cljs.core.disj.cljs$core$IFn$_invoke$arity$2(G__72853__$1,cljs.core.cst$kw$up):G__72853__$1);
var G__72853__$3 = ((cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(x,(org.nfrac.comportex.demos.q_learning_2d.grid_w - (1))))?cljs.core.disj.cljs$core$IFn$_invoke$arity$2(G__72853__$2,cljs.core.cst$kw$right):G__72853__$2);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(y,(org.nfrac.comportex.demos.q_learning_2d.grid_h - (1)))){
return cljs.core.disj.cljs$core$IFn$_invoke$arity$2(G__72853__$3,cljs.core.cst$kw$down);
} else {
return G__72853__$3;
}
});
org.nfrac.comportex.demos.q_learning_2d.column__GT_signal = cljs.core.zipmap(cljs.core.range.cljs$core$IFn$_invoke$arity$0(),(function (){var iter__6925__auto__ = (function org$nfrac$comportex$demos$q_learning_2d$iter__72854(s__72855){
return (new cljs.core.LazySeq(null,(function (){
var s__72855__$1 = s__72855;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__72855__$1);
if(temp__4657__auto__){
var xs__5205__auto__ = temp__4657__auto__;
var motion = cljs.core.first(xs__5205__auto__);
var iterys__6921__auto__ = ((function (s__72855__$1,motion,xs__5205__auto__,temp__4657__auto__){
return (function org$nfrac$comportex$demos$q_learning_2d$iter__72854_$_iter__72856(s__72857){
return (new cljs.core.LazySeq(null,((function (s__72855__$1,motion,xs__5205__auto__,temp__4657__auto__){
return (function (){
var s__72857__$1 = s__72857;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__72857__$1);
if(temp__4657__auto____$1){
var s__72857__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__72857__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__72857__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__72859 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__72858 = (0);
while(true){
if((i__72858 < size__6924__auto__)){
var influence = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__72858);
cljs.core.chunk_append(b__72859,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [motion,influence], null));

var G__72865 = (i__72858 + (1));
i__72858 = G__72865;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__72859),org$nfrac$comportex$demos$q_learning_2d$iter__72854_$_iter__72856(cljs.core.chunk_rest(s__72857__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__72859),null);
}
} else {
var influence = cljs.core.first(s__72857__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [motion,influence], null),org$nfrac$comportex$demos$q_learning_2d$iter__72854_$_iter__72856(cljs.core.rest(s__72857__$2)));
}
} else {
return null;
}
break;
}
});})(s__72855__$1,motion,xs__5205__auto__,temp__4657__auto__))
,null,null));
});})(s__72855__$1,motion,xs__5205__auto__,temp__4657__auto__))
;
var fs__6922__auto__ = cljs.core.seq(iterys__6921__auto__(cljs.core.repeat.cljs$core$IFn$_invoke$arity$2((10),1.0)));
if(fs__6922__auto__){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2(fs__6922__auto__,org$nfrac$comportex$demos$q_learning_2d$iter__72854(cljs.core.rest(s__72855__$1)));
} else {
var G__72866 = cljs.core.rest(s__72855__$1);
s__72855__$1 = G__72866;
continue;
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$up,cljs.core.cst$kw$down,cljs.core.cst$kw$left,cljs.core.cst$kw$right], null));
})());
org.nfrac.comportex.demos.q_learning_2d.select_action = (function org$nfrac$comportex$demos$q_learning_2d$select_action(htm,curr_pos){
var alyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3], null));
var acols = org.nfrac.comportex.protocols.active_columns(alyr);
var signals = cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.demos.q_learning_2d.column__GT_signal,acols);
var poss = org.nfrac.comportex.demos.q_learning_2d.possible_directions(curr_pos);
var G__72874 = cljs.core.key(cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core.max_key,cljs.core.val,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(cljs.core.comp.cljs$core$IFn$_invoke$arity$2(poss,cljs.core.key),cljs.core.persistent_BANG_(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (alyr,acols,signals,poss){
return (function (m,p__72875){
var vec__72876 = p__72875;
var motion = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72876,(0),null);
var influence = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72876,(1),null);
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(m,motion,(cljs.core.get.cljs$core$IFn$_invoke$arity$3(m,motion,(0)) + influence));
});})(alyr,acols,signals,poss))
,cljs.core.transient$(cljs.core.PersistentArrayMap.EMPTY),signals)))));
return (org.nfrac.comportex.demos.q_learning_2d.direction__GT_action.cljs$core$IFn$_invoke$arity$1 ? org.nfrac.comportex.demos.q_learning_2d.direction__GT_action.cljs$core$IFn$_invoke$arity$1(G__72874) : org.nfrac.comportex.demos.q_learning_2d.direction__GT_action.call(null,G__72874));
});
org.nfrac.comportex.demos.q_learning_2d.apply_action = (function org$nfrac$comportex$demos$q_learning_2d$apply_action(inval){
var x = cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(inval);
var y = cljs.core.cst$kw$y.cljs$core$IFn$_invoke$arity$1(inval);
var dx = cljs.core.cst$kw$dx.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval));
var dy = cljs.core.cst$kw$dy.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval));
var next_x = (function (){var x__6484__auto__ = (function (){var x__6491__auto__ = (x + dx);
var y__6492__auto__ = (org.nfrac.comportex.demos.q_learning_2d.grid_w - (1));
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})();
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var next_y = (function (){var x__6484__auto__ = (function (){var x__6491__auto__ = (y + dy);
var y__6492__auto__ = (org.nfrac.comportex.demos.q_learning_2d.grid_h - (1));
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})();
var y__6485__auto__ = (0);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var next_z = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.demos.q_learning_2d.surface,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [next_x,next_y], null));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(inval,cljs.core.cst$kw$x,next_x,cljs.core.array_seq([cljs.core.cst$kw$y,next_y,cljs.core.cst$kw$z,next_z], 0));
});
org.nfrac.comportex.demos.q_learning_2d.make_model = (function org$nfrac$comportex$demos$q_learning_2d$make_model(){
var sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.encoders.vec_selector.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.cst$kw$x,cljs.core.cst$kw$y], 0)),org.nfrac.comportex.encoders.coordinate_encoder(org.nfrac.comportex.demos.q_learning_2d.input_dim,org.nfrac.comportex.demos.q_learning_2d.n_on_bits,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.q_learning_2d.surface_coord_scale,org.nfrac.comportex.demos.q_learning_2d.surface_coord_scale], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.q_learning_2d.coord_radius,org.nfrac.comportex.demos.q_learning_2d.coord_radius], null))], null);
var dx_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$action,cljs.core.cst$kw$dx], null),org.nfrac.comportex.encoders.linear_encoder.cljs$core$IFn$_invoke$arity$3(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(100)], null),(30),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(-1),(1)], null))], null);
var dy_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$action,cljs.core.cst$kw$dy], null),org.nfrac.comportex.encoders.linear_encoder.cljs$core$IFn$_invoke$arity$3(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(100)], null),(30),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(-1),(1)], null))], null);
var msensor = org.nfrac.comportex.encoders.sensor_cat.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([dx_sensor,dy_sensor], 0));
return org.nfrac.comportex.core.region_network(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$rgn_DASH_1,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,cljs.core.cst$kw$motor], null),cljs.core.cst$kw$action,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rgn_DASH_1], null)], null),cljs.core.constantly(org.nfrac.comportex.core.sensory_region),new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$rgn_DASH_1,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(org.nfrac.comportex.demos.q_learning_2d.spec,cljs.core.cst$kw$lateral_DASH_synapses_QMARK_,false),cljs.core.cst$kw$action,org.nfrac.comportex.demos.q_learning_2d.action_spec], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,sensor], null),new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$input,sensor,cljs.core.cst$kw$motor,msensor], null));
});
org.nfrac.comportex.demos.q_learning_2d.htm_step_with_action_selection = (function org$nfrac$comportex$demos$q_learning_2d$htm_step_with_action_selection(world_c){
return (function (htm,inval){
var htm_a = org.nfrac.comportex.protocols.htm_learn(org.nfrac.comportex.protocols.htm_activate(org.nfrac.comportex.protocols.htm_sense(htm,inval,cljs.core.cst$kw$sensory)));
var reward = (0.01 * cljs.core.cst$kw$z.cljs$core$IFn$_invoke$arity$1(inval));
var terminal_state_QMARK_ = (org.nfrac.comportex.util.abs(cljs.core.cst$kw$z.cljs$core$IFn$_invoke$arity$1(inval)) >= (100));
var upd_htm = (cljs.core.truth_(cljs.core.cst$kw$prev_DASH_action.cljs$core$IFn$_invoke$arity$1(inval))?org.nfrac.comportex.demos.q_learning_1d.q_learn(htm_a,htm,reward):cljs.core.assoc_in(htm_a,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3,cljs.core.cst$kw$Q_DASH_info], null),cljs.core.PersistentArrayMap.EMPTY));
var info = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(upd_htm,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3,cljs.core.cst$kw$Q_DASH_info], null));
var newQ = (function (){var x__6491__auto__ = (function (){var x__6484__auto__ = (cljs.core.cst$kw$Q_DASH_old.cljs$core$IFn$_invoke$arity$2(info,(0)) + cljs.core.cst$kw$adj.cljs$core$IFn$_invoke$arity$2(info,(0)));
var y__6485__auto__ = -1.0;
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var y__6492__auto__ = 1.0;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})();
var Q_map = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.cst$kw$Q_DASH_map.cljs$core$IFn$_invoke$arity$1(inval),cljs.core.select_keys(inval,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$x,cljs.core.cst$kw$y,cljs.core.cst$kw$action], null)),newQ);
var action = org.nfrac.comportex.demos.q_learning_2d.select_action(upd_htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(inval),cljs.core.cst$kw$y.cljs$core$IFn$_invoke$arity$1(inval)], null));
var inval_with_action = cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(inval,cljs.core.cst$kw$action,action,cljs.core.array_seq([cljs.core.cst$kw$prev_DASH_action,cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval),cljs.core.cst$kw$Q_DASH_map,Q_map], 0));
var new_inval_72879 = ((terminal_state_QMARK_)?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(org.nfrac.comportex.demos.q_learning_2d.initial_inval,cljs.core.cst$kw$Q_DASH_map,Q_map):org.nfrac.comportex.demos.q_learning_2d.apply_action(inval_with_action));
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(world_c,new_inval_72879);

var G__72878 = upd_htm;
var G__72878__$1 = org.nfrac.comportex.protocols.htm_sense(G__72878,inval_with_action,cljs.core.cst$kw$motor)
;
var G__72878__$2 = org.nfrac.comportex.protocols.htm_depolarise(G__72878__$1)
;
if(terminal_state_QMARK_){
return org.nfrac.comportex.protocols.break$(G__72878__$2,cljs.core.cst$kw$tm);
} else {
return G__72878__$2;
}
});
});
