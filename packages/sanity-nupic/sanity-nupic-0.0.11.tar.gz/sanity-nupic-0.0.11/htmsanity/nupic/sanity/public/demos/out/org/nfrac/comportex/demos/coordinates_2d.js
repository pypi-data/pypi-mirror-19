// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.demos.coordinates_2d');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.encoders');
goog.require('org.nfrac.comportex.util');
org.nfrac.comportex.demos.coordinates_2d.input_dim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(30),(30)], null);
org.nfrac.comportex.demos.coordinates_2d.n_on_bits = (30);
org.nfrac.comportex.demos.coordinates_2d.max_pos = (45);
org.nfrac.comportex.demos.coordinates_2d.max_vel = (5);
org.nfrac.comportex.demos.coordinates_2d.radius = (15);
org.nfrac.comportex.demos.coordinates_2d.spec = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(20),(50)], null),cljs.core.cst$kw$depth,(8)], null);
org.nfrac.comportex.demos.coordinates_2d.higher_level_spec = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(20),(20)], null),cljs.core.cst$kw$proximal,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$max_DASH_segments,(5)], null)], null);
org.nfrac.comportex.demos.coordinates_2d.initial_input_val = new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$x,(-10),cljs.core.cst$kw$y,(-20),cljs.core.cst$kw$vx,(1),cljs.core.cst$kw$vy,(1),cljs.core.cst$kw$ax,(1),cljs.core.cst$kw$ay,(1)], null);
org.nfrac.comportex.demos.coordinates_2d.clamp_vec = (function org$nfrac$comportex$demos$coordinates_2d$clamp_vec(p__72284,max_mag){
var vec__72287 = p__72284;
var vx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72287,(0),null);
var vy = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72287,(1),null);
var mag = (function (){var G__72288 = ((vx * vx) + (vy * vy));
return Math.sqrt(G__72288);
})();
var scale = (max_mag / mag);
if((mag > max_mag)){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(vx * scale),(vy * scale)], null);
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [vx,vy], null);
}
});
org.nfrac.comportex.demos.coordinates_2d.wrap = (function org$nfrac$comportex$demos$coordinates_2d$wrap(x,lim){
return (cljs.core.mod((x + lim),((2) * lim)) - lim);
});
org.nfrac.comportex.demos.coordinates_2d.input_transform = (function org$nfrac$comportex$demos$coordinates_2d$input_transform(p__72289){
var map__72293 = p__72289;
var map__72293__$1 = ((((!((map__72293 == null)))?((((map__72293.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72293.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72293):map__72293);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72293__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72293__$1,cljs.core.cst$kw$y);
var vx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72293__$1,cljs.core.cst$kw$vx);
var vy = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72293__$1,cljs.core.cst$kw$vy);
var ax = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72293__$1,cljs.core.cst$kw$ax);
var ay = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72293__$1,cljs.core.cst$kw$ay);
var vec__72295 = org.nfrac.comportex.demos.coordinates_2d.clamp_vec(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(vx + ax),(vy + ay)], null),org.nfrac.comportex.demos.coordinates_2d.max_vel);
var vx2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72295,(0),null);
var vy2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72295,(1),null);
var x2 = (x + vx);
var y2 = (y + vy);
return new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$x,org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.coordinates_2d.wrap(x2,org.nfrac.comportex.demos.coordinates_2d.max_pos)),cljs.core.cst$kw$y,org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.coordinates_2d.wrap(y2,org.nfrac.comportex.demos.coordinates_2d.max_pos)),cljs.core.cst$kw$vx,vx2,cljs.core.cst$kw$vy,vy2,cljs.core.cst$kw$ax,((cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2((y > (0)),(y2 > (0))))?(ax * (-1)):ax),cljs.core.cst$kw$ay,((cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2((x > (0)),(x2 > (0))))?(ay * (-1)):ay)], null);
});
/**
 * Returns an infinite lazy seq of sensory input values.
 */
org.nfrac.comportex.demos.coordinates_2d.input_seq = (function org$nfrac$comportex$demos$coordinates_2d$input_seq(){
return cljs.core.iterate(org.nfrac.comportex.demos.coordinates_2d.input_transform,org.nfrac.comportex.demos.coordinates_2d.initial_input_val);
});
org.nfrac.comportex.demos.coordinates_2d.sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.encoders.vec_selector.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.cst$kw$x,cljs.core.cst$kw$y], 0)),org.nfrac.comportex.encoders.coordinate_encoder(org.nfrac.comportex.demos.coordinates_2d.input_dim,org.nfrac.comportex.demos.coordinates_2d.n_on_bits,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1),(1)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.coordinates_2d.radius,org.nfrac.comportex.demos.coordinates_2d.radius], null))], null);
org.nfrac.comportex.demos.coordinates_2d.n_region_model = (function org$nfrac$comportex$demos$coordinates_2d$n_region_model(var_args){
var args72296 = [];
var len__7211__auto___72299 = arguments.length;
var i__7212__auto___72300 = (0);
while(true){
if((i__7212__auto___72300 < len__7211__auto___72299)){
args72296.push((arguments[i__7212__auto___72300]));

var G__72301 = (i__7212__auto___72300 + (1));
i__7212__auto___72300 = G__72301;
continue;
} else {
}
break;
}

var G__72298 = args72296.length;
switch (G__72298) {
case 1:
return org.nfrac.comportex.demos.coordinates_2d.n_region_model.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.nfrac.comportex.demos.coordinates_2d.n_region_model.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args72296.length)].join('')));

}
});

org.nfrac.comportex.demos.coordinates_2d.n_region_model.cljs$core$IFn$_invoke$arity$1 = (function (n){
return org.nfrac.comportex.demos.coordinates_2d.n_region_model.cljs$core$IFn$_invoke$arity$2(n,org.nfrac.comportex.demos.coordinates_2d.spec);
});

org.nfrac.comportex.demos.coordinates_2d.n_region_model.cljs$core$IFn$_invoke$arity$2 = (function (n,spec){
return org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$4(n,org.nfrac.comportex.core.sensory_region,cljs.core.list_STAR_.cljs$core$IFn$_invoke$arity$2(spec,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.coordinates_2d.higher_level_spec)),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,org.nfrac.comportex.demos.coordinates_2d.sensor], null));
});

org.nfrac.comportex.demos.coordinates_2d.n_region_model.cljs$lang$maxFixedArity = 2;
