// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.demos.letters');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.encoders');
goog.require('org.nfrac.comportex.util');
goog.require('clojure.string');
org.nfrac.comportex.demos.letters.bit_width = (500);
org.nfrac.comportex.demos.letters.n_on_bits = (25);
org.nfrac.comportex.demos.letters.spec = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1000)], null),cljs.core.cst$kw$depth,(8),cljs.core.cst$kw$distal,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$perm_DASH_init,0.21], null),cljs.core.cst$kw$distal_DASH_vs_DASH_proximal_DASH_weight,0.2], null);
org.nfrac.comportex.demos.letters.higher_level_spec = org.nfrac.comportex.util.deep_merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([org.nfrac.comportex.demos.letters.spec,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(800)], null),cljs.core.cst$kw$proximal,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$max_DASH_segments,(5)], null)], null)], 0));
org.nfrac.comportex.demos.letters.clean_text = (function org$nfrac$comportex$demos$letters$clean_text(text){
return clojure.string.replace(clojure.string.lower_case(text),/\s+/," ");
});
org.nfrac.comportex.demos.letters.random_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$value,org.nfrac.comportex.encoders.unique_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.letters.bit_width], null),org.nfrac.comportex.demos.letters.n_on_bits)], null);
org.nfrac.comportex.demos.letters.n_region_model = (function org$nfrac$comportex$demos$letters$n_region_model(var_args){
var args71803 = [];
var len__7211__auto___71806 = arguments.length;
var i__7212__auto___71807 = (0);
while(true){
if((i__7212__auto___71807 < len__7211__auto___71806)){
args71803.push((arguments[i__7212__auto___71807]));

var G__71808 = (i__7212__auto___71807 + (1));
i__7212__auto___71807 = G__71808;
continue;
} else {
}
break;
}

var G__71805 = args71803.length;
switch (G__71805) {
case 1:
return org.nfrac.comportex.demos.letters.n_region_model.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.nfrac.comportex.demos.letters.n_region_model.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args71803.length)].join('')));

}
});

org.nfrac.comportex.demos.letters.n_region_model.cljs$core$IFn$_invoke$arity$1 = (function (n){
return org.nfrac.comportex.demos.letters.n_region_model.cljs$core$IFn$_invoke$arity$2(n,org.nfrac.comportex.demos.letters.spec);
});

org.nfrac.comportex.demos.letters.n_region_model.cljs$core$IFn$_invoke$arity$2 = (function (n,spec){
return org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$4(n,org.nfrac.comportex.core.sensory_region,cljs.core.list_STAR_.cljs$core$IFn$_invoke$arity$2(spec,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.letters.higher_level_spec)),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,org.nfrac.comportex.demos.letters.random_sensor], null));
});

org.nfrac.comportex.demos.letters.n_region_model.cljs$lang$maxFixedArity = 2;
