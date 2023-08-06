// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.demos.sensorimotor_1d');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.encoders');
goog.require('org.nfrac.comportex.util');
goog.require('clojure.test.check.random');
org.nfrac.comportex.demos.sensorimotor_1d.bit_width = (300);
org.nfrac.comportex.demos.sensorimotor_1d.motor_bit_width = (100);
org.nfrac.comportex.demos.sensorimotor_1d.motor_n_on_bits = (25);
org.nfrac.comportex.demos.sensorimotor_1d.world_size = (10);
org.nfrac.comportex.demos.sensorimotor_1d.items = new cljs.core.PersistentVector(null, 10, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$a,cljs.core.cst$kw$b,cljs.core.cst$kw$c,cljs.core.cst$kw$d,cljs.core.cst$kw$e,cljs.core.cst$kw$f,cljs.core.cst$kw$g,cljs.core.cst$kw$h,cljs.core.cst$kw$i,cljs.core.cst$kw$j], null);
org.nfrac.comportex.demos.sensorimotor_1d.saccades = new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(-1),(0),(1),(2)], null);
org.nfrac.comportex.demos.sensorimotor_1d.higher_level_spec_diff = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(800)], null),cljs.core.cst$kw$proximal,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$max_DASH_segments,(5),cljs.core.cst$kw$new_DASH_synapse_DASH_count,(12),cljs.core.cst$kw$learn_DASH_threshold,(6)], null)], null);
org.nfrac.comportex.demos.sensorimotor_1d.spec = new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(800)], null),cljs.core.cst$kw$depth,(5),cljs.core.cst$kw$proximal,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$perm_DASH_inc,0.1,cljs.core.cst$kw$perm_DASH_dec,0.01], null),cljs.core.cst$kw$distal,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$punish_QMARK_,false], null),cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.demos.sensorimotor_1d.higher_level_spec_diff], null);
org.nfrac.comportex.demos.sensorimotor_1d.higher_level_spec = org.nfrac.comportex.util.deep_merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([org.nfrac.comportex.demos.sensorimotor_1d.spec,org.nfrac.comportex.demos.sensorimotor_1d.higher_level_spec_diff], 0));
org.nfrac.comportex.demos.sensorimotor_1d.fields = cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,(function (){var iter__6925__auto__ = (function org$nfrac$comportex$demos$sensorimotor_1d$iter__70717(s__70718){
return (new cljs.core.LazySeq(null,(function (){
var s__70718__$1 = s__70718;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__70718__$1);
if(temp__4657__auto__){
var s__70718__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__70718__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__70718__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__70720 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__70719 = (0);
while(true){
if((i__70719 < size__6924__auto__)){
var k = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__70719);
cljs.core.chunk_append(b__70720,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [k,cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(cljs.core.comp.cljs$core$IFn$_invoke$arity$2(cljs.core.keyword,cljs.core.str),cljs.core.name(k))], null));

var G__70723 = (i__70719 + (1));
i__70719 = G__70723;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__70720),org$nfrac$comportex$demos$sensorimotor_1d$iter__70717(cljs.core.chunk_rest(s__70718__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__70720),null);
}
} else {
var k = cljs.core.first(s__70718__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [k,cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(cljs.core.comp.cljs$core$IFn$_invoke$arity$2(cljs.core.keyword,cljs.core.str),cljs.core.name(k))], null),org$nfrac$comportex$demos$sensorimotor_1d$iter__70717(cljs.core.rest(s__70718__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$abcdefghij,cljs.core.cst$kw$baggagejade,cljs.core.cst$kw$baggagefeed,cljs.core.cst$kw$beachjadehigh,cljs.core.cst$kw$deafjigjag,cljs.core.cst$kw$hidebadface,cljs.core.cst$kw$hidefacebad], null));
})());
org.nfrac.comportex.demos.sensorimotor_1d.initial_world = (function org$nfrac$comportex$demos$sensorimotor_1d$initial_world(field,seed){
return cljs.core.vary_meta.cljs$core$IFn$_invoke$arity$4(new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,field,cljs.core.cst$kw$position,cljs.core.quot(cljs.core.count(field),(2)),cljs.core.cst$kw$next_DASH_saccade,(1)], null),cljs.core.assoc,cljs.core.cst$kw$org$nfrac$comportex$demos$sensorimotor_DASH_1d_SLASH_rng,clojure.test.check.random.make_random.cljs$core$IFn$_invoke$arity$1(seed));
});
org.nfrac.comportex.demos.sensorimotor_1d.world_transform = (function org$nfrac$comportex$demos$sensorimotor_1d$world_transform(m){
var n = cljs.core.count(cljs.core.cst$kw$field.cljs$core$IFn$_invoke$arity$1(m));
var dx = cljs.core.cst$kw$next_DASH_saccade.cljs$core$IFn$_invoke$arity$1(m);
var x = cljs.core.mod((cljs.core.cst$kw$position.cljs$core$IFn$_invoke$arity$1(m) + dx),n);
var vec__70725 = clojure.test.check.random.split(cljs.core.cst$kw$org$nfrac$comportex$demos$sensorimotor_DASH_1d_SLASH_rng.cljs$core$IFn$_invoke$arity$1(cljs.core.meta(m)));
var rng = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70725,(0),null);
var rng_STAR_ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70725,(1),null);
var sacc = org.nfrac.comportex.util.rand_nth(rng_STAR_,org.nfrac.comportex.demos.sensorimotor_1d.saccades);
return cljs.core.vary_meta.cljs$core$IFn$_invoke$arity$4(cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(m,cljs.core.cst$kw$position,x,cljs.core.array_seq([cljs.core.cst$kw$last_DASH_saccade,dx,cljs.core.cst$kw$next_DASH_saccade,sacc], 0)),cljs.core.assoc,cljs.core.cst$kw$org$nfrac$comportex$demos$sensorimotor_DASH_1d_SLASH_rng,rng);
});
org.nfrac.comportex.demos.sensorimotor_1d.attach_current_value = (function org$nfrac$comportex$demos$sensorimotor_1d$attach_current_value(m){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(m,cljs.core.cst$kw$value,cljs.core.get.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$field.cljs$core$IFn$_invoke$arity$1(m),cljs.core.cst$kw$position.cljs$core$IFn$_invoke$arity$1(m)));
});
/**
 * Returns an infinite lazy seq of sensory input values.
 */
org.nfrac.comportex.demos.sensorimotor_1d.input_seq = (function org$nfrac$comportex$demos$sensorimotor_1d$input_seq(world){
return cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.demos.sensorimotor_1d.attach_current_value,cljs.core.iterate(org.nfrac.comportex.demos.sensorimotor_1d.world_transform,world));
});
org.nfrac.comportex.demos.sensorimotor_1d.block_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$value,org.nfrac.comportex.encoders.category_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.sensorimotor_1d.bit_width], null),org.nfrac.comportex.demos.sensorimotor_1d.items)], null);
org.nfrac.comportex.demos.sensorimotor_1d.block_motor_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$next_DASH_saccade,org.nfrac.comportex.encoders.linear_encoder.cljs$core$IFn$_invoke$arity$3(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.sensorimotor_1d.motor_bit_width], null),org.nfrac.comportex.demos.sensorimotor_1d.motor_n_on_bits,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.first(org.nfrac.comportex.demos.sensorimotor_1d.saccades),cljs.core.last(org.nfrac.comportex.demos.sensorimotor_1d.saccades)], null))], null);
org.nfrac.comportex.demos.sensorimotor_1d.n_region_model = (function org$nfrac$comportex$demos$sensorimotor_1d$n_region_model(var_args){
var args70726 = [];
var len__7211__auto___70729 = arguments.length;
var i__7212__auto___70730 = (0);
while(true){
if((i__7212__auto___70730 < len__7211__auto___70729)){
args70726.push((arguments[i__7212__auto___70730]));

var G__70731 = (i__7212__auto___70730 + (1));
i__7212__auto___70730 = G__70731;
continue;
} else {
}
break;
}

var G__70728 = args70726.length;
switch (G__70728) {
case 1:
return org.nfrac.comportex.demos.sensorimotor_1d.n_region_model.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.nfrac.comportex.demos.sensorimotor_1d.n_region_model.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args70726.length)].join('')));

}
});

org.nfrac.comportex.demos.sensorimotor_1d.n_region_model.cljs$core$IFn$_invoke$arity$1 = (function (n){
return org.nfrac.comportex.demos.sensorimotor_1d.n_region_model.cljs$core$IFn$_invoke$arity$2(n,org.nfrac.comportex.demos.sensorimotor_1d.spec);
});

org.nfrac.comportex.demos.sensorimotor_1d.n_region_model.cljs$core$IFn$_invoke$arity$2 = (function (n,spec){
return org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$5(n,org.nfrac.comportex.core.sensorimotor_region,cljs.core.list_STAR_.cljs$core$IFn$_invoke$arity$2(spec,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.sensorimotor_1d.higher_level_spec)),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,org.nfrac.comportex.demos.sensorimotor_1d.block_sensor], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$motor,org.nfrac.comportex.demos.sensorimotor_1d.block_motor_sensor], null));
});

org.nfrac.comportex.demos.sensorimotor_1d.n_region_model.cljs$lang$maxFixedArity = 2;
