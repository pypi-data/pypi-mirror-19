// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.cortical_io');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.topology');
goog.require('cljs_http.client');
goog.require('cljs.core.async');
goog.require('org.nfrac.comportex.util');
goog.require('org.nfrac.comportex.encoders');
goog.require('clojure.string');
org.nfrac.comportex.cortical_io.base_uri = "http://api.cortical.io/rest";
org.nfrac.comportex.cortical_io.query_params = new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$retina_name,"en_associative"], null);
org.nfrac.comportex.cortical_io.retina_dim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(128),(128)], null);
org.nfrac.comportex.cortical_io.retina_size = cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core._STAR_,org.nfrac.comportex.cortical_io.retina_dim);
org.nfrac.comportex.cortical_io.max_bits = (512);
org.nfrac.comportex.cortical_io.min_votes = (2);
org.nfrac.comportex.cortical_io.request_fingerprint = (function org$nfrac$comportex$cortical_io$request_fingerprint(api_key,term){
return cljs_http.client.post.cljs$core$IFn$_invoke$arity$variadic([cljs.core.str(org.nfrac.comportex.cortical_io.base_uri),cljs.core.str("/expressions")].join(''),cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$query_DASH_params,org.nfrac.comportex.cortical_io.query_params,cljs.core.cst$kw$content_DASH_type,"application/json",cljs.core.cst$kw$as,cljs.core.cst$kw$json,cljs.core.cst$kw$json_DASH_params,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$term,term], null),cljs.core.cst$kw$with_DASH_credentials_QMARK_,false,cljs.core.cst$kw$throw_DASH_exceptions,false,cljs.core.cst$kw$headers,new cljs.core.PersistentArrayMap(null, 1, ["api-key",api_key], null)], null)], 0));
});
org.nfrac.comportex.cortical_io.request_similar_terms = (function org$nfrac$comportex$cortical_io$request_similar_terms(api_key,bits,max_n){
return cljs_http.client.post.cljs$core$IFn$_invoke$arity$variadic([cljs.core.str(org.nfrac.comportex.cortical_io.base_uri),cljs.core.str("/expressions/similar_terms")].join(''),cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$query_DASH_params,cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(org.nfrac.comportex.cortical_io.query_params,cljs.core.cst$kw$get_fingerprint,true,cljs.core.array_seq([cljs.core.cst$kw$max_results,max_n], 0)),cljs.core.cst$kw$content_DASH_type,"application/json",cljs.core.cst$kw$as,cljs.core.cst$kw$json,cljs.core.cst$kw$json_DASH_params,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$positions,cljs.core.sort.cljs$core$IFn$_invoke$arity$1(bits)], null),cljs.core.cst$kw$with_DASH_credentials_QMARK_,false,cljs.core.cst$kw$throw_DASH_exceptions,false,cljs.core.cst$kw$headers,new cljs.core.PersistentArrayMap(null, 1, ["api-key",api_key], null)], null)], 0));
});
org.nfrac.comportex.cortical_io.random_sdr = (function org$nfrac$comportex$cortical_io$random_sdr(term){
return org.nfrac.comportex.encoders.unique_sdr(term,org.nfrac.comportex.cortical_io.retina_size,(org.nfrac.comportex.cortical_io.retina_size * 0.02));
});
/**
 * Maps a retina fingerprint index to another index which is spatially
 * scrambled. Meaning that direct neighbours in the retina are now
 * offset from each other by around 17 units. This is a complete
 * mapping, i.e. the following holds:
 * 
 * `
 * (= (set (map scramble-bit (range retina-size)))
 *    (set (range retina-size)))`.
 */
org.nfrac.comportex.cortical_io.scramble_bit = (function org$nfrac$comportex$cortical_io$scramble_bit(i){
return cljs.core.mod((i * (17)),org.nfrac.comportex.cortical_io.retina_size);
});
org.nfrac.comportex.cortical_io.unscramble_bit = (function org$nfrac$comportex$cortical_io$unscramble_bit(j){
return cljs.core.quot(((cljs.core.mod((cljs.core.rem(j,(17)) * (13)),(17)) * org.nfrac.comportex.cortical_io.retina_size) + j),(17));
});
org.nfrac.comportex.cortical_io.scramble_bitset = (function org$nfrac$comportex$cortical_io$scramble_bitset(bits){
return cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.cortical_io.scramble_bit,bits);
});
/**
 * assoc, but not if the key already has a (truthy) value.
 */
org.nfrac.comportex.cortical_io._QMARK_assoc = (function org$nfrac$comportex$cortical_io$_QMARK_assoc(m,k,v){
if(cljs.core.truth_((m.cljs$core$IFn$_invoke$arity$1 ? m.cljs$core$IFn$_invoke$arity$1(k) : m.call(null,k)))){
return m;
} else {
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(m,k,v);
}
});
/**
 * Makes a request to cortical.io to look up the fingerprint for the
 * term, and stores it in the given cache atom. In Clojure this is a
 * synchonous call and returns the fingerprint bit-set. In
 * Clojurescript this is an asynchronous call and returns a channel.
 */
org.nfrac.comportex.cortical_io.cache_fingerprint_BANG_ = (function org$nfrac$comportex$cortical_io$cache_fingerprint_BANG_(api_key,cache,term){
var term__$1 = clojure.string.lower_case(term);
var handle = ((function (term__$1){
return (function (result){
if(cljs.core.truth_((function (){var G__71748 = cljs.core.cst$kw$status.cljs$core$IFn$_invoke$arity$1(result);
return (cljs_http.client.unexceptional_status_QMARK_.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.unexceptional_status_QMARK_.cljs$core$IFn$_invoke$arity$1(G__71748) : cljs_http.client.unexceptional_status_QMARK_.call(null,G__71748));
})())){
return cljs.core.set(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(result,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$body,cljs.core.cst$kw$positions], null)));
} else {
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["cortical.io lookup of term failed:",term__$1], 0));

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([result], 0));

return org.nfrac.comportex.cortical_io.random_sdr(term__$1);
}
});})(term__$1))
;
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,term__$1,handle){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,term__$1,handle){
return (function (state_71755){
var state_val_71756 = (state_71755[(1)]);
if((state_val_71756 === (1))){
var inst_71749 = org.nfrac.comportex.cortical_io.request_fingerprint(api_key,term__$1);
var state_71755__$1 = state_71755;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71755__$1,(2),inst_71749);
} else {
if((state_val_71756 === (2))){
var inst_71751 = (state_71755[(2)]);
var inst_71752 = handle(inst_71751);
var inst_71753 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(cache,org.nfrac.comportex.cortical_io._QMARK_assoc,term__$1,inst_71752);
var state_71755__$1 = state_71755;
return cljs.core.async.impl.ioc_helpers.return_chan(state_71755__$1,inst_71753);
} else {
return null;
}
}
});})(c__38109__auto__,term__$1,handle))
;
return ((function (switch__37995__auto__,c__38109__auto__,term__$1,handle){
return (function() {
var org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto__ = null;
var org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_71760 = [null,null,null,null,null,null,null];
(statearr_71760[(0)] = org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto__);

(statearr_71760[(1)] = (1));

return statearr_71760;
});
var org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto____1 = (function (state_71755){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71755);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71761){if((e71761 instanceof Object)){
var ex__37999__auto__ = e71761;
var statearr_71762_71764 = state_71755;
(statearr_71762_71764[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71755);

return cljs.core.cst$kw$recur;
} else {
throw e71761;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__71765 = state_71755;
state_71755 = G__71765;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto__ = function(state_71755){
switch(arguments.length){
case 0:
return org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto____1.call(this,state_71755);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto____0;
org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto____1;
return org$nfrac$comportex$cortical_io$cache_fingerprint_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,term__$1,handle))
})();
var state__38111__auto__ = (function (){var statearr_71763 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71763[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_71763;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,term__$1,handle))
);

return c__38109__auto__;
});
/**
 * Looks up a fingerprint for the term, being a set of active indices,
 * in the cache. If it is not found (which should not happen, it
 * should be preloaded from the web service), the term is assigned a
 * new random SDR.
 */
org.nfrac.comportex.cortical_io.get_fingerprint = (function org$nfrac$comportex$cortical_io$get_fingerprint(cache,term){
var term__$1 = clojure.string.lower_case(term);
var or__6153__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(cache) : cljs.core.deref.call(null,cache)),term__$1);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.get.cljs$core$IFn$_invoke$arity$2(cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(cache,org.nfrac.comportex.cortical_io._QMARK_assoc,term__$1,(function (){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["no fingerprint in cache for term:",term__$1,"- generating a random one"], 0));

return org.nfrac.comportex.cortical_io.random_sdr(term__$1);
})()
),term__$1);
}
});
org.nfrac.comportex.cortical_io.elect_bits = (function org$nfrac$comportex$cortical_io$elect_bits(bit_votes,min_votes,max_bits){
var min_votes__$1 = min_votes;
while(true){
var bits = cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (min_votes__$1){
return (function (p__71768){
var vec__71769 = p__71768;
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71769,(0),null);
var n = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71769,(1),null);
if((n >= min_votes__$1)){
return i;
} else {
return null;
}
});})(min_votes__$1))
,bit_votes);
if((cljs.core.count(bits) > max_bits)){
var G__71770 = (min_votes__$1 + (1));
min_votes__$1 = G__71770;
continue;
} else {
return bits;
}
break;
}
});
org.nfrac.comportex.cortical_io.cortical_io_encoder = (function org$nfrac$comportex$cortical_io$cortical_io_encoder(var_args){
var args__7218__auto__ = [];
var len__7211__auto___71796 = arguments.length;
var i__7212__auto___71797 = (0);
while(true){
if((i__7212__auto___71797 < len__7211__auto___71796)){
args__7218__auto__.push((arguments[i__7212__auto___71797]));

var G__71798 = (i__7212__auto___71797 + (1));
i__7212__auto___71797 = G__71798;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((2) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((2)),(0))):null);
return org.nfrac.comportex.cortical_io.cortical_io_encoder.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),(arguments[(1)]),argseq__7219__auto__);
});

org.nfrac.comportex.cortical_io.cortical_io_encoder.cljs$core$IFn$_invoke$arity$variadic = (function (api_key,cache,p__71774){
var map__71775 = p__71774;
var map__71775__$1 = ((((!((map__71775 == null)))?((((map__71775.cljs$lang$protocol_mask$partition0$ & (64))) || (map__71775.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__71775):map__71775);
var decode_locally_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__71775__$1,cljs.core.cst$kw$decode_DASH_locally_QMARK_);
var spatial_scramble_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__71775__$1,cljs.core.cst$kw$spatial_DASH_scramble_QMARK_);
var topo = org.nfrac.comportex.topology.make_topology(org.nfrac.comportex.cortical_io.retina_dim);
if(typeof org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777 !== 'undefined'){
} else {

/**
* @constructor
 * @implements {org.nfrac.comportex.protocols.PEncoder}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.IWithMeta}
 * @implements {org.nfrac.comportex.protocols.PTopological}
*/
org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777 = (function (api_key,cache,p__71774,map__71775,decode_locally_QMARK_,spatial_scramble_QMARK_,topo,meta71778){
this.api_key = api_key;
this.cache = cache;
this.p__71774 = p__71774;
this.map__71775 = map__71775;
this.decode_locally_QMARK_ = decode_locally_QMARK_;
this.spatial_scramble_QMARK_ = spatial_scramble_QMARK_;
this.topo = topo;
this.meta71778 = meta71778;
this.cljs$lang$protocol_mask$partition0$ = 393216;
this.cljs$lang$protocol_mask$partition1$ = 0;
})
org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (_71779,meta71778__$1){
var self__ = this;
var _71779__$1 = this;
return (new org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777(self__.api_key,self__.cache,self__.p__71774,self__.map__71775,self__.decode_locally_QMARK_,self__.spatial_scramble_QMARK_,self__.topo,meta71778__$1));
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.prototype.cljs$core$IMeta$_meta$arity$1 = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (_71779){
var self__ = this;
var _71779__$1 = this;
return self__.meta71778;
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (_){
var self__ = this;
var ___$1 = this;
return self__.topo;
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.prototype.org$nfrac$comportex$protocols$PEncoder$ = true;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.prototype.org$nfrac$comportex$protocols$PEncoder$encode$arity$2 = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (_,term){
var self__ = this;
var ___$1 = this;
if(cljs.core.seq(term)){
var G__71780 = org.nfrac.comportex.cortical_io.get_fingerprint(self__.cache,term);
if(cljs.core.truth_(self__.spatial_scramble_QMARK_)){
return org.nfrac.comportex.cortical_io.scramble_bitset(G__71780);
} else {
return G__71780;
}
} else {
return cljs.core.sequence.cljs$core$IFn$_invoke$arity$1(null);
}
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.prototype.org$nfrac$comportex$protocols$PEncoder$decode$arity$3 = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (this$,bit_votes,n){
var self__ = this;
var this$__$1 = this;
var bit_votes__$1 = (cljs.core.truth_(self__.spatial_scramble_QMARK_)?cljs.core.zipmap(cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.cortical_io.unscramble_bit,cljs.core.keys(bit_votes)),cljs.core.vals(bit_votes)):bit_votes);
if(cljs.core.truth_(self__.decode_locally_QMARK_)){
return cljs.core.take.cljs$core$IFn$_invoke$arity$2(n,org.nfrac.comportex.encoders.decode_by_brute_force(this$__$1,cljs.core.keys((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(self__.cache) : cljs.core.deref.call(null,self__.cache))),bit_votes__$1));
} else {
var bits = org.nfrac.comportex.cortical_io.elect_bits(bit_votes__$1,org.nfrac.comportex.cortical_io.min_votes,org.nfrac.comportex.cortical_io.max_bits);
if(cljs.core.empty_QMARK_(bits)){
return cljs.core.PersistentVector.EMPTY;
} else {
var total_votes = cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core._PLUS_,cljs.core.vals(bit_votes__$1));
var handle = ((function (total_votes,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (result){
if(cljs.core.truth_((function (){var G__71781 = cljs.core.cst$kw$status.cljs$core$IFn$_invoke$arity$1(result);
return (cljs_http.client.unexceptional_status_QMARK_.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.unexceptional_status_QMARK_.cljs$core$IFn$_invoke$arity$1(G__71781) : cljs_http.client.unexceptional_status_QMARK_.call(null,G__71781));
})())){
return cljs.core.take.cljs$core$IFn$_invoke$arity$2(n,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (total_votes,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (item){
var x_bits = cljs.core.set(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(item,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$fingerprint,cljs.core.cst$kw$positions], null)));
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["received prediction results."], 0));

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["x-bits =",x_bits], 0));

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["bits =",bits], 0));

return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(org.nfrac.comportex.encoders.prediction_stats(x_bits,bit_votes__$1,total_votes),cljs.core.cst$kw$value,cljs.core.get.cljs$core$IFn$_invoke$arity$2(item,cljs.core.cst$kw$term));
});})(total_votes,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
,cljs.core.cst$kw$body.cljs$core$IFn$_invoke$arity$1(result)));
} else {
return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([result], 0));
}
});})(total_votes,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;
return new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$channel,(function (){var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,total_votes,handle,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,total_votes,handle,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (state_71787){
var state_val_71788 = (state_71787[(1)]);
if((state_val_71788 === (1))){
var inst_71782 = org.nfrac.comportex.cortical_io.request_similar_terms(self__.api_key,bits,n);
var state_71787__$1 = state_71787;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71787__$1,(2),inst_71782);
} else {
if((state_val_71788 === (2))){
var inst_71784 = (state_71787[(2)]);
var inst_71785 = handle(inst_71784);
var state_71787__$1 = state_71787;
return cljs.core.async.impl.ioc_helpers.return_chan(state_71787__$1,inst_71785);
} else {
return null;
}
}
});})(c__38109__auto__,total_votes,handle,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;
return ((function (switch__37995__auto__,c__38109__auto__,total_votes,handle,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function() {
var org$nfrac$comportex$cortical_io$state_machine__37996__auto__ = null;
var org$nfrac$comportex$cortical_io$state_machine__37996__auto____0 = (function (){
var statearr_71792 = [null,null,null,null,null,null,null];
(statearr_71792[(0)] = org$nfrac$comportex$cortical_io$state_machine__37996__auto__);

(statearr_71792[(1)] = (1));

return statearr_71792;
});
var org$nfrac$comportex$cortical_io$state_machine__37996__auto____1 = (function (state_71787){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71787);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71793){if((e71793 instanceof Object)){
var ex__37999__auto__ = e71793;
var statearr_71794_71799 = state_71787;
(statearr_71794_71799[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71787);

return cljs.core.cst$kw$recur;
} else {
throw e71793;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__71800 = state_71787;
state_71787 = G__71800;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$nfrac$comportex$cortical_io$state_machine__37996__auto__ = function(state_71787){
switch(arguments.length){
case 0:
return org$nfrac$comportex$cortical_io$state_machine__37996__auto____0.call(this);
case 1:
return org$nfrac$comportex$cortical_io$state_machine__37996__auto____1.call(this,state_71787);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$nfrac$comportex$cortical_io$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$nfrac$comportex$cortical_io$state_machine__37996__auto____0;
org$nfrac$comportex$cortical_io$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$nfrac$comportex$cortical_io$state_machine__37996__auto____1;
return org$nfrac$comportex$cortical_io$state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,total_votes,handle,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
})();
var state__38111__auto__ = (function (){var statearr_71795 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71795[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_71795;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,total_votes,handle,bits,bit_votes__$1,this$__$1,topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
);

return c__38109__auto__;
})()], null);
}
}
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.getBasis = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (){
return new cljs.core.PersistentVector(null, 8, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$api_DASH_key,cljs.core.cst$sym$cache,cljs.core.cst$sym$p__71774,cljs.core.cst$sym$map__71775,cljs.core.cst$sym$decode_DASH_locally_QMARK_,cljs.core.cst$sym$spatial_DASH_scramble_QMARK_,cljs.core.cst$sym$topo,cljs.core.cst$sym$meta71778], null);
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.cljs$lang$type = true;

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.cljs$lang$ctorStr = "org.nfrac.comportex.cortical-io/t_org$nfrac$comportex$cortical_io71777";

org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777.cljs$lang$ctorPrWriter = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function (this__6751__auto__,writer__6752__auto__,opt__6753__auto__){
return cljs.core._write(writer__6752__auto__,"org.nfrac.comportex.cortical-io/t_org$nfrac$comportex$cortical_io71777");
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

org.nfrac.comportex.cortical_io.__GT_t_org$nfrac$comportex$cortical_io71777 = ((function (topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_){
return (function org$nfrac$comportex$cortical_io$__GT_t_org$nfrac$comportex$cortical_io71777(api_key__$1,cache__$1,p__71774__$1,map__71775__$2,decode_locally_QMARK___$1,spatial_scramble_QMARK___$1,topo__$1,meta71778){
return (new org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777(api_key__$1,cache__$1,p__71774__$1,map__71775__$2,decode_locally_QMARK___$1,spatial_scramble_QMARK___$1,topo__$1,meta71778));
});})(topo,map__71775,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_))
;

}

return (new org.nfrac.comportex.cortical_io.t_org$nfrac$comportex$cortical_io71777(api_key,cache,p__71774,map__71775__$1,decode_locally_QMARK_,spatial_scramble_QMARK_,topo,cljs.core.PersistentArrayMap.EMPTY));
});

org.nfrac.comportex.cortical_io.cortical_io_encoder.cljs$lang$maxFixedArity = (2);

org.nfrac.comportex.cortical_io.cortical_io_encoder.cljs$lang$applyTo = (function (seq71771){
var G__71772 = cljs.core.first(seq71771);
var seq71771__$1 = cljs.core.next(seq71771);
var G__71773 = cljs.core.first(seq71771__$1);
var seq71771__$2 = cljs.core.next(seq71771__$1);
return org.nfrac.comportex.cortical_io.cortical_io_encoder.cljs$core$IFn$_invoke$arity$variadic(G__71772,G__71773,seq71771__$2);
});
