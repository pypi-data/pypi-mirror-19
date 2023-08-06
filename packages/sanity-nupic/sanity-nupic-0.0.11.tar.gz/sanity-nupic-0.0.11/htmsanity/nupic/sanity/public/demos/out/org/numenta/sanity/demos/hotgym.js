// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.hotgym');
goog.require('cljs.core');
goog.require('goog.dom');
goog.require('org.nfrac.comportex.cells');
goog.require('reagent.core');
goog.require('org.numenta.sanity.viz_canvas');
goog.require('org.numenta.sanity.main');
goog.require('org.nfrac.comportex.protocols');
goog.require('goog.net.XhrIo');
goog.require('org.numenta.sanity.util');
goog.require('org.numenta.sanity.comportex.data');
goog.require('org.nfrac.comportex.topology');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('reagent_forms.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.numenta.sanity.bridge.browser');
goog.require('org.numenta.sanity.demos.comportex_common');
goog.require('org.nfrac.comportex.util');
goog.require('org.nfrac.comportex.encoders');
goog.require('cljs.reader');
org.numenta.sanity.demos.hotgym.world_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.demos.hotgym.into_sim = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.demos.hotgym.model = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
/**
 * By example:
 *   Given 7.2, returns (7, 8, 6, 9, 5, 10, ...),
 *   Given 7.7, returns (8, 7, 9, 6, 10, 5, ...)
 */
org.numenta.sanity.demos.hotgym.middle_out_range = (function org$numenta$sanity$demos$hotgym$middle_out_range(v){
var start = cljs.core.long$(Math.round(v));
var rounded_down_QMARK_ = (v > start);
var up = cljs.core.iterate(cljs.core.inc,start);
var down = cljs.core.iterate(cljs.core.dec,start);
if(rounded_down_QMARK_){
return cljs.core.interleave.cljs$core$IFn$_invoke$arity$2(down,cljs.core.drop.cljs$core$IFn$_invoke$arity$2((1),up));
} else {
return cljs.core.interleave.cljs$core$IFn$_invoke$arity$2(up,cljs.core.drop.cljs$core$IFn$_invoke$arity$2((1),down));
}
});
org.numenta.sanity.demos.hotgym.multiples_within_radius = (function org$numenta$sanity$demos$hotgym$multiples_within_radius(center,radius,multiples_of){
var lower_bound = (center - radius);
var upper_bound = (center + radius);
return cljs.core.take_while.cljs$core$IFn$_invoke$arity$2(((function (lower_bound,upper_bound){
return (function (p1__71004_SHARP_){
return ((lower_bound <= p1__71004_SHARP_)) && ((p1__71004_SHARP_ <= upper_bound));
});})(lower_bound,upper_bound))
,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.partial.cljs$core$IFn$_invoke$arity$2(cljs.core._STAR_,multiples_of),org.numenta.sanity.demos.hotgym.middle_out_range((center / multiples_of))));
});
/**
 * Move items from `from` to `coll` until its size reaches `max-size`
 *   or we run out of items. Specifically supports sets and maps, which don't
 *   always grow when an item is added.
 */
org.numenta.sanity.demos.hotgym.into_bounded = (function org$numenta$sanity$demos$hotgym$into_bounded(coll,max_size,from){
var coll__$1 = coll;
var from__$1 = from;
while(true){
var n_remaining = (max_size - cljs.core.count(coll__$1));
if(cljs.core.truth_((function (){var and__6141__auto__ = (n_remaining > (0));
if(and__6141__auto__){
return cljs.core.not_empty(from__$1);
} else {
return and__6141__auto__;
}
})())){
var vec__71006 = cljs.core.split_at(n_remaining,from__$1);
var taken = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71006,(0),null);
var untaken = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71006,(1),null);
var G__71007 = cljs.core.into.cljs$core$IFn$_invoke$arity$2(coll__$1,taken);
var G__71008 = untaken;
coll__$1 = G__71007;
from__$1 = G__71008;
continue;
} else {
return coll__$1;
}
break;
}
});
/**
 * Place a bit in the center.
 *   Distribute bits around the center until we've used half of the remainder.
 *   Double the density. Distribute again until we've used half of the remainder.
 *   Double the density. ...
 *   Continue until all active bits are distributed or all bits are active.
 * 
 *   Strategically choose bit positions so that the intersections between
 *   various ranges will select the same bits.
 */
org.numenta.sanity.demos.hotgym.sampled_window = (function org$numenta$sanity$demos$hotgym$sampled_window(center,n_bits,target_n_active,bit_radius){
var chosen = cljs.core.PersistentHashSet.fromArray([center], true);
var density = (((target_n_active - cljs.core.count(chosen)) / ((2) * bit_radius)) / (2));
while(true){
var remaining = (target_n_active - cljs.core.count(chosen));
var multiples_of = cljs.core.long$(((1) / density));
if(((remaining > (0))) && ((multiples_of > (0)))){
var half_remaining = cljs.core.quot(remaining,(2));
var n_take = (((cljs.core.odd_QMARK_(remaining)) || (cljs.core.odd_QMARK_(half_remaining)))?remaining:half_remaining);
var G__71010 = org.numenta.sanity.demos.hotgym.into_bounded(chosen,(n_take + cljs.core.count(chosen)),cljs.core.filter.cljs$core$IFn$_invoke$arity$2(((function (chosen,density,half_remaining,n_take,remaining,multiples_of){
return (function (p1__71009_SHARP_){
return (((0) <= p1__71009_SHARP_)) && ((p1__71009_SHARP_ <= (n_bits - (1))));
});})(chosen,density,half_remaining,n_take,remaining,multiples_of))
,org.numenta.sanity.demos.hotgym.multiples_within_radius(center,bit_radius,multiples_of)));
var G__71011 = (density * (2));
chosen = G__71010;
density = G__71011;
continue;
} else {
return chosen;
}
break;
}
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.nfrac.comportex.protocols.PEncoder}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PTopological}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.numenta.sanity.demos.hotgym.SamplingLinearEncoder = (function (topo,n_active,lower,upper,radius,__meta,__extmap,__hash){
this.topo = topo;
this.n_active = n_active;
this.lower = lower;
this.upper = upper;
this.radius = radius;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k71013,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__71015 = (((k71013 instanceof cljs.core.Keyword))?k71013.fqn:null);
switch (G__71015) {
case "topo":
return self__.topo;

break;
case "n-active":
return self__.n_active;

break;
case "lower":
return self__.lower;

break;
case "upper":
return self__.upper;

break;
case "radius":
return self__.radius;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k71013,else__6770__auto__);

}
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.topo;
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.demos.hotgym.SamplingLinearEncoder{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$n_DASH_active,self__.n_active],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$lower,self__.lower],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$upper,self__.upper],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$radius,self__.radius],null))], null),self__.__extmap));
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__71012){
var self__ = this;
var G__71012__$1 = this;
return (new cljs.core.RecordIter((0),G__71012__$1,5,new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$topo,cljs.core.cst$kw$n_DASH_active,cljs.core.cst$kw$lower,cljs.core.cst$kw$upper,cljs.core.cst$kw$radius], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,self__.n_active,self__.lower,self__.upper,self__.radius,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (5 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
var self__ = this;
var this__6762__auto____$1 = this;
var h__6588__auto__ = self__.__hash;
if(!((h__6588__auto__ == null))){
return h__6588__auto__;
} else {
var h__6588__auto____$1 = cljs.core.hash_imap(this__6762__auto____$1);
self__.__hash = h__6588__auto____$1;

return h__6588__auto____$1;
}
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
var self__ = this;
var this__6763__auto____$1 = this;
if(cljs.core.truth_((function (){var and__6141__auto__ = other__6764__auto__;
if(cljs.core.truth_(and__6141__auto__)){
var and__6141__auto____$1 = (this__6763__auto____$1.constructor === other__6764__auto__.constructor);
if(and__6141__auto____$1){
return cljs.core.equiv_map(this__6763__auto____$1,other__6764__auto__);
} else {
return and__6141__auto____$1;
}
} else {
return and__6141__auto__;
}
})())){
return true;
} else {
return false;
}
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.org$nfrac$comportex$protocols$PEncoder$ = true;

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.org$nfrac$comportex$protocols$PEncoder$encode$arity$2 = (function (_,x){
var self__ = this;
var ___$1 = this;
if(cljs.core.truth_(x)){
var n_bits = org.nfrac.comportex.protocols.size(self__.topo);
var domain_width = (self__.upper - self__.lower);
var center = cljs.core.long$(((((function (){var x__6491__auto__ = (function (){var x__6484__auto__ = x;
var y__6485__auto__ = self__.lower;
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var y__6492__auto__ = self__.upper;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})() - self__.lower) / domain_width) * n_bits));
var bit_radius = (self__.radius * (org.nfrac.comportex.protocols.size(self__.topo) / domain_width));
return org.numenta.sanity.demos.hotgym.sampled_window(center,n_bits,self__.n_active,bit_radius);
} else {
return cljs.core.sequence.cljs$core$IFn$_invoke$arity$1(null);
}
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.org$nfrac$comportex$protocols$PEncoder$decode$arity$3 = (function (this$,bit_votes,n){
var self__ = this;
var this$__$1 = this;
var span = (self__.upper - self__.lower);
var values = cljs.core.range.cljs$core$IFn$_invoke$arity$3(self__.lower,self__.upper,(((((5) < span)) && ((span < (250))))?(1):(span / (50))));
return cljs.core.take.cljs$core$IFn$_invoke$arity$2(n,org.nfrac.comportex.encoders.decode_by_brute_force(this$__$1,values,bit_votes));
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$upper,null,cljs.core.cst$kw$topo,null,cljs.core.cst$kw$radius,null,cljs.core.cst$kw$lower,null,cljs.core.cst$kw$n_DASH_active,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,self__.n_active,self__.lower,self__.upper,self__.radius,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__71012){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__71016 = cljs.core.keyword_identical_QMARK_;
var expr__71017 = k__6775__auto__;
if(cljs.core.truth_((pred__71016.cljs$core$IFn$_invoke$arity$2 ? pred__71016.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$topo,expr__71017) : pred__71016.call(null,cljs.core.cst$kw$topo,expr__71017)))){
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(G__71012,self__.n_active,self__.lower,self__.upper,self__.radius,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__71016.cljs$core$IFn$_invoke$arity$2 ? pred__71016.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$n_DASH_active,expr__71017) : pred__71016.call(null,cljs.core.cst$kw$n_DASH_active,expr__71017)))){
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,G__71012,self__.lower,self__.upper,self__.radius,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__71016.cljs$core$IFn$_invoke$arity$2 ? pred__71016.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$lower,expr__71017) : pred__71016.call(null,cljs.core.cst$kw$lower,expr__71017)))){
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,self__.n_active,G__71012,self__.upper,self__.radius,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__71016.cljs$core$IFn$_invoke$arity$2 ? pred__71016.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$upper,expr__71017) : pred__71016.call(null,cljs.core.cst$kw$upper,expr__71017)))){
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,self__.n_active,self__.lower,G__71012,self__.radius,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__71016.cljs$core$IFn$_invoke$arity$2 ? pred__71016.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$radius,expr__71017) : pred__71016.call(null,cljs.core.cst$kw$radius,expr__71017)))){
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,self__.n_active,self__.lower,self__.upper,G__71012,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,self__.n_active,self__.lower,self__.upper,self__.radius,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__71012),null));
}
}
}
}
}
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$n_DASH_active,self__.n_active],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$lower,self__.lower],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$upper,self__.upper],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$radius,self__.radius],null))], null),self__.__extmap));
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__71012){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(self__.topo,self__.n_active,self__.lower,self__.upper,self__.radius,G__71012,self__.__extmap,self__.__hash));
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.getBasis = (function (){
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$topo,cljs.core.cst$sym$n_DASH_active,cljs.core.cst$sym$lower,cljs.core.cst$sym$upper,cljs.core.cst$sym$radius], null);
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.cljs$lang$type = true;

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.demos.hotgym/SamplingLinearEncoder");
});

org.numenta.sanity.demos.hotgym.SamplingLinearEncoder.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.demos.hotgym/SamplingLinearEncoder");
});

org.numenta.sanity.demos.hotgym.__GT_SamplingLinearEncoder = (function org$numenta$sanity$demos$hotgym$__GT_SamplingLinearEncoder(topo,n_active,lower,upper,radius){
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(topo,n_active,lower,upper,radius,null,null,null));
});

org.numenta.sanity.demos.hotgym.map__GT_SamplingLinearEncoder = (function org$numenta$sanity$demos$hotgym$map__GT_SamplingLinearEncoder(G__71014){
return (new org.numenta.sanity.demos.hotgym.SamplingLinearEncoder(cljs.core.cst$kw$topo.cljs$core$IFn$_invoke$arity$1(G__71014),cljs.core.cst$kw$n_DASH_active.cljs$core$IFn$_invoke$arity$1(G__71014),cljs.core.cst$kw$lower.cljs$core$IFn$_invoke$arity$1(G__71014),cljs.core.cst$kw$upper.cljs$core$IFn$_invoke$arity$1(G__71014),cljs.core.cst$kw$radius.cljs$core$IFn$_invoke$arity$1(G__71014),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__71014,cljs.core.cst$kw$topo,cljs.core.array_seq([cljs.core.cst$kw$n_DASH_active,cljs.core.cst$kw$lower,cljs.core.cst$kw$upper,cljs.core.cst$kw$radius], 0)),null));
});

/**
 * A linear encoder that samples the surrounding radius, rather than
 *   activating all of it. Sampling density decreases as distance increases.
 * 
 *   * `dimensions` is the size of the encoder in bits along one or more
 *  dimensions, a vector e.g. [500].
 * 
 *   * `n-active` is the number of bits to be active.
 * 
 *   * `[lower upper]` gives the numeric range to cover. The input number
 *  will be clamped to this range.
 * 
 *   * `radius` describes the range to sample.
 * 
 *   Recommendations:
 * 
 *   * `lower` and `upper` should be `radius` below and above the actual
 *  lower and upper bounds. Otherwise the radius will extend off the
 *  number line, creating representations that behave a bit differently
 *  from the rest.
 */
org.numenta.sanity.demos.hotgym.sampling_linear_encoder = (function org$numenta$sanity$demos$hotgym$sampling_linear_encoder(dimensions,n_active,p__71020,radius){
var vec__71022 = p__71020;
var lower = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71022,(0),null);
var upper = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71022,(1),null);
var topo = org.nfrac.comportex.topology.make_topology(dimensions);
return org.numenta.sanity.demos.hotgym.map__GT_SamplingLinearEncoder(new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$topo,topo,cljs.core.cst$kw$n_DASH_active,n_active,cljs.core.cst$kw$lower,lower,cljs.core.cst$kw$upper,upper,cljs.core.cst$kw$radius,radius], null));
});
org.numenta.sanity.demos.hotgym.anomaly_score = (function org$numenta$sanity$demos$hotgym$anomaly_score(p__71023){
var map__71026 = p__71023;
var map__71026__$1 = ((((!((map__71026 == null)))?((((map__71026.cljs$lang$protocol_mask$partition0$ & (64))) || (map__71026.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__71026):map__71026);
var active = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__71026__$1,cljs.core.cst$kw$active);
var active_predicted = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__71026__$1,cljs.core.cst$kw$active_DASH_predicted);
var total = (active + active_predicted);
if((total > (0))){
return (active / total);
} else {
return (1);
}
});
org.numenta.sanity.demos.hotgym.consider_consumption_BANG_ = (function org$numenta$sanity$demos$hotgym$consider_consumption_BANG_(step__GT_scores,step,consumption){
var candidate = new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$consumption,consumption], null);
var out_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var snapshot_id = cljs.core.cst$kw$snapshot_DASH_id.cljs$core$IFn$_invoke$arity$1(step);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, ["consider-future",snapshot_id,candidate,org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(out_c,true)], null));

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,candidate,out_c,snapshot_id){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,candidate,out_c,snapshot_id){
return (function (state_71066){
var state_val_71067 = (state_71066[(1)]);
if((state_val_71067 === (1))){
var state_71066__$1 = state_71066;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71066__$1,(2),out_c);
} else {
if((state_val_71067 === (2))){
var inst_71055 = (state_71066[(2)]);
var inst_71056 = cljs.core.seq(inst_71055);
var inst_71057 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_71056,(0),null);
var inst_71058 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_71057,(0),null);
var inst_71059 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_71057,(1),null);
var inst_71060 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_71061 = [step,consumption];
var inst_71062 = (new cljs.core.PersistentVector(null,2,(5),inst_71060,inst_71061,null));
var inst_71063 = org.numenta.sanity.demos.hotgym.anomaly_score(inst_71059);
var inst_71064 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(step__GT_scores,cljs.core.assoc_in,inst_71062,inst_71063);
var state_71066__$1 = (function (){var statearr_71068 = state_71066;
(statearr_71068[(7)] = inst_71058);

return statearr_71068;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_71066__$1,inst_71064);
} else {
return null;
}
}
});})(c__38109__auto__,candidate,out_c,snapshot_id))
;
return ((function (switch__37995__auto__,c__38109__auto__,candidate,out_c,snapshot_id){
return (function() {
var org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_71072 = [null,null,null,null,null,null,null,null];
(statearr_71072[(0)] = org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto__);

(statearr_71072[(1)] = (1));

return statearr_71072;
});
var org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto____1 = (function (state_71066){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71066);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71073){if((e71073 instanceof Object)){
var ex__37999__auto__ = e71073;
var statearr_71074_71076 = state_71066;
(statearr_71074_71076[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71066);

return cljs.core.cst$kw$recur;
} else {
throw e71073;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__71077 = state_71066;
state_71066 = G__71077;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto__ = function(state_71066){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto____1.call(this,state_71066);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$hotgym$consider_consumption_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,candidate,out_c,snapshot_id))
})();
var state__38111__auto__ = (function (){var statearr_71075 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71075[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_71075;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,candidate,out_c,snapshot_id))
);

return c__38109__auto__;
});
org.numenta.sanity.demos.hotgym.try_boundaries_QMARK_ = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(true);
org.numenta.sanity.demos.hotgym.try_last_value_QMARK_ = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(true);
org.numenta.sanity.demos.hotgym.n_predictions = reagent.core.atom.cljs$core$IFn$_invoke$arity$1((3));
org.numenta.sanity.demos.hotgym.unit_width = (8);
org.numenta.sanity.demos.hotgym.cx = (org.numenta.sanity.demos.hotgym.unit_width / (2));
org.numenta.sanity.demos.hotgym.max_r = org.numenta.sanity.demos.hotgym.cx;
org.numenta.sanity.demos.hotgym.actual_svg = (function org$numenta$sanity$demos$hotgym$actual_svg(step,top,unit_height){
var actual_consumption = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(step,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input_DASH_value,cljs.core.cst$kw$consumption], null));
var y_actual = ((top - actual_consumption) * unit_height);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rect,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(y_actual - 1.5),cljs.core.cst$kw$width,org.numenta.sanity.demos.hotgym.unit_width,cljs.core.cst$kw$height,(3),cljs.core.cst$kw$fill,"black"], null)], null);
});
org.numenta.sanity.demos.hotgym.prediction_svg = (function org$numenta$sanity$demos$hotgym$prediction_svg(y_scores){
var min_score = cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.min,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.second,y_scores));
var candidates = cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.first,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(((function (min_score){
return (function (p__71082){
var vec__71083 = p__71082;
var consumption = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71083,(0),null);
var score = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71083,(1),null);
return cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(score,min_score);
});})(min_score))
,y_scores));
var vec__71081 = cljs.core.nth.cljs$core$IFn$_invoke$arity$2(candidates,cljs.core.quot(cljs.core.count(candidates),(2)));
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71081,(0),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rect,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(y - (1)),cljs.core.cst$kw$width,org.numenta.sanity.demos.hotgym.unit_width,cljs.core.cst$kw$height,(2),cljs.core.cst$kw$fill,"#78B4FB"], null)], null);
});
org.numenta.sanity.demos.hotgym.anomaly_gradient_svg = (function org$numenta$sanity$demos$hotgym$anomaly_gradient_svg(y_scores){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g], null),(function (){var iter__6925__auto__ = (function org$numenta$sanity$demos$hotgym$anomaly_gradient_svg_$_iter__71102(s__71103){
return (new cljs.core.LazySeq(null,(function (){
var s__71103__$1 = s__71103;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__71103__$1);
if(temp__4657__auto__){
var s__71103__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__71103__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71103__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71105 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71104 = (0);
while(true){
if((i__71104 < size__6924__auto__)){
var vec__71114 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71104);
var vec__71115 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71114,(0),null);
var y1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71115,(0),null);
var score1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71115,(1),null);
var vec__71116 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71114,(1),null);
var y2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71116,(0),null);
var score2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71116,(1),null);
var grad_id = [cljs.core.str(cljs.core.random_uuid())].join('');
cljs.core.chunk_append(b__71105,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$defs,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$linearGradient,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$id,grad_id,cljs.core.cst$kw$x1,(0),cljs.core.cst$kw$y1,(0),cljs.core.cst$kw$x2,(0),cljs.core.cst$kw$y2,(1)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$stop,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$offset,"0%",cljs.core.cst$kw$stop_DASH_color,"red",cljs.core.cst$kw$stop_DASH_opacity,score1], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$stop,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$offset,"100%",cljs.core.cst$kw$stop_DASH_color,"red",cljs.core.cst$kw$stop_DASH_opacity,score2], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rect,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$x,(org.numenta.sanity.demos.hotgym.cx - org.numenta.sanity.demos.hotgym.max_r),cljs.core.cst$kw$y,y1,cljs.core.cst$kw$width,((2) * org.numenta.sanity.demos.hotgym.max_r),cljs.core.cst$kw$height,(y2 - y1),cljs.core.cst$kw$fill,[cljs.core.str("url(#"),cljs.core.str(grad_id),cljs.core.str(")")].join('')], null)], null)], null));

var G__71120 = (i__71104 + (1));
i__71104 = G__71120;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71105),org$numenta$sanity$demos$hotgym$anomaly_gradient_svg_$_iter__71102(cljs.core.chunk_rest(s__71103__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71105),null);
}
} else {
var vec__71117 = cljs.core.first(s__71103__$2);
var vec__71118 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71117,(0),null);
var y1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71118,(0),null);
var score1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71118,(1),null);
var vec__71119 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71117,(1),null);
var y2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71119,(0),null);
var score2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71119,(1),null);
var grad_id = [cljs.core.str(cljs.core.random_uuid())].join('');
return cljs.core.cons(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$defs,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$linearGradient,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$id,grad_id,cljs.core.cst$kw$x1,(0),cljs.core.cst$kw$y1,(0),cljs.core.cst$kw$x2,(0),cljs.core.cst$kw$y2,(1)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$stop,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$offset,"0%",cljs.core.cst$kw$stop_DASH_color,"red",cljs.core.cst$kw$stop_DASH_opacity,score1], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$stop,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$offset,"100%",cljs.core.cst$kw$stop_DASH_color,"red",cljs.core.cst$kw$stop_DASH_opacity,score2], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rect,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$x,(org.numenta.sanity.demos.hotgym.cx - org.numenta.sanity.demos.hotgym.max_r),cljs.core.cst$kw$y,y1,cljs.core.cst$kw$width,((2) * org.numenta.sanity.demos.hotgym.max_r),cljs.core.cst$kw$height,(y2 - y1),cljs.core.cst$kw$fill,[cljs.core.str("url(#"),cljs.core.str(grad_id),cljs.core.str(")")].join('')], null)], null)], null),org$numenta$sanity$demos$hotgym$anomaly_gradient_svg_$_iter__71102(cljs.core.rest(s__71103__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.partition.cljs$core$IFn$_invoke$arity$3((2),(1),cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.first,y_scores)));
})());
});
org.numenta.sanity.demos.hotgym.anomaly_samples_svg = (function org$numenta$sanity$demos$hotgym$anomaly_samples_svg(ys){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g], null),(function (){var iter__6925__auto__ = (function org$numenta$sanity$demos$hotgym$anomaly_samples_svg_$_iter__71127(s__71128){
return (new cljs.core.LazySeq(null,(function (){
var s__71128__$1 = s__71128;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__71128__$1);
if(temp__4657__auto__){
var s__71128__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__71128__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71128__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71130 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71129 = (0);
while(true){
if((i__71129 < size__6924__auto__)){
var y = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71129);
cljs.core.chunk_append(b__71130,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$circle,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$fill,"brown",cljs.core.cst$kw$cx,org.numenta.sanity.demos.hotgym.cx,cljs.core.cst$kw$cy,y,cljs.core.cst$kw$r,1.5], null)], null));

var G__71133 = (i__71129 + (1));
i__71129 = G__71133;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71130),org$numenta$sanity$demos$hotgym$anomaly_samples_svg_$_iter__71127(cljs.core.chunk_rest(s__71128__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71130),null);
}
} else {
var y = cljs.core.first(s__71128__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$circle,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$fill,"brown",cljs.core.cst$kw$cx,org.numenta.sanity.demos.hotgym.cx,cljs.core.cst$kw$cy,y,cljs.core.cst$kw$r,1.5], null)], null),org$numenta$sanity$demos$hotgym$anomaly_samples_svg_$_iter__71127(cljs.core.rest(s__71128__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(ys);
})());
});
org.numenta.sanity.demos.hotgym.consumption_axis_svg = (function org$numenta$sanity$demos$hotgym$consumption_axis_svg(h,bottom,top){
var label_every = (10);
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g], null),(function (){var iter__6925__auto__ = ((function (label_every){
return (function org$numenta$sanity$demos$hotgym$consumption_axis_svg_$_iter__71140(s__71141){
return (new cljs.core.LazySeq(null,((function (label_every){
return (function (){
var s__71141__$1 = s__71141;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__71141__$1);
if(temp__4657__auto__){
var s__71141__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__71141__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71141__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71143 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71142 = (0);
while(true){
if((i__71142 < size__6924__auto__)){
var i = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71142);
cljs.core.chunk_append(b__71143,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$text,new cljs.core.PersistentArrayMap(null, 8, [cljs.core.cst$kw$x,(-5),cljs.core.cst$kw$y,(h * ((1) - ((i - bottom) / (top - bottom)))),cljs.core.cst$kw$dy,"0.35em",cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$fill,"rgb(104, 104, 104)",cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$font_DASH_weight,"bold"], null),cljs.core.cst$kw$text_DASH_anchor,"end"], null),[cljs.core.str(i)].join('')], null));

var G__71146 = (i__71142 + (1));
i__71142 = G__71146;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71143),org$numenta$sanity$demos$hotgym$consumption_axis_svg_$_iter__71140(cljs.core.chunk_rest(s__71141__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71143),null);
}
} else {
var i = cljs.core.first(s__71141__$2);
return cljs.core.cons(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$text,new cljs.core.PersistentArrayMap(null, 8, [cljs.core.cst$kw$x,(-5),cljs.core.cst$kw$y,(h * ((1) - ((i - bottom) / (top - bottom)))),cljs.core.cst$kw$dy,"0.35em",cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$fill,"rgb(104, 104, 104)",cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$font_DASH_weight,"bold"], null),cljs.core.cst$kw$text_DASH_anchor,"end"], null),[cljs.core.str(i)].join('')], null),org$numenta$sanity$demos$hotgym$consumption_axis_svg_$_iter__71140(cljs.core.rest(s__71141__$2)));
}
} else {
return null;
}
break;
}
});})(label_every))
,null,null));
});})(label_every))
;
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$3(bottom,top,label_every));
})());
});
org.numenta.sanity.demos.hotgym.extend_past_px = (30);
org.numenta.sanity.demos.hotgym.horizontal_label = (function org$numenta$sanity$demos$hotgym$horizontal_label(x,y,w,transition_QMARK_,contents_above,contents_below){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$position,"relative"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 8, [cljs.core.cst$kw$position,"absolute",cljs.core.cst$kw$left,x,cljs.core.cst$kw$top,(y - 0.5),cljs.core.cst$kw$width,((w - x) + org.numenta.sanity.demos.hotgym.extend_past_px),cljs.core.cst$kw$transition_DASH_property,(cljs.core.truth_(transition_QMARK_)?"top":"none"),cljs.core.cst$kw$transition_DASH_duration,"0.15s",cljs.core.cst$kw$height,(1),cljs.core.cst$kw$background_DASH_color,"black"], null)], null)], null)], null),(function (){var iter__6925__auto__ = (function org$numenta$sanity$demos$hotgym$horizontal_label_$_iter__71157(s__71158){
return (new cljs.core.LazySeq(null,(function (){
var s__71158__$1 = s__71158;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__71158__$1);
if(temp__4657__auto__){
var s__71158__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__71158__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71158__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71160 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71159 = (0);
while(true){
if((i__71159 < size__6924__auto__)){
var vec__71165 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71159);
var contents = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71165,(0),null);
var top = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71165,(1),null);
if(cljs.core.truth_(contents)){
cljs.core.chunk_append(b__71160,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 8, [cljs.core.cst$kw$position,"absolute",cljs.core.cst$kw$top,y,cljs.core.cst$kw$transition_DASH_property,(cljs.core.truth_(transition_QMARK_)?"top":"none"),cljs.core.cst$kw$transition_DASH_duration,"0.15s",cljs.core.cst$kw$left,w,cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$font_DASH_weight,"bold"], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$position,"absolute",cljs.core.cst$kw$top,top,cljs.core.cst$kw$transition_DASH_property,"top",cljs.core.cst$kw$transition_DASH_duration,"0.15s",cljs.core.cst$kw$left,(4)], null)], null),contents], null)], null));

var G__71167 = (i__71159 + (1));
i__71159 = G__71167;
continue;
} else {
var G__71168 = (i__71159 + (1));
i__71159 = G__71168;
continue;
}
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71160),org$numenta$sanity$demos$hotgym$horizontal_label_$_iter__71157(cljs.core.chunk_rest(s__71158__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71160),null);
}
} else {
var vec__71166 = cljs.core.first(s__71158__$2);
var contents = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71166,(0),null);
var top = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71166,(1),null);
if(cljs.core.truth_(contents)){
return cljs.core.cons(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 8, [cljs.core.cst$kw$position,"absolute",cljs.core.cst$kw$top,y,cljs.core.cst$kw$transition_DASH_property,(cljs.core.truth_(transition_QMARK_)?"top":"none"),cljs.core.cst$kw$transition_DASH_duration,"0.15s",cljs.core.cst$kw$left,w,cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$font_DASH_weight,"bold"], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$position,"absolute",cljs.core.cst$kw$top,top,cljs.core.cst$kw$transition_DASH_property,"top",cljs.core.cst$kw$transition_DASH_duration,"0.15s",cljs.core.cst$kw$left,(4)], null)], null),contents], null)], null),org$numenta$sanity$demos$hotgym$horizontal_label_$_iter__71157(cljs.core.rest(s__71158__$2)));
} else {
var G__71169 = cljs.core.rest(s__71158__$2);
s__71158__$1 = G__71169;
continue;
}
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [contents_above,"-2.7em"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [contents_below,"0.2em"], null)], null));
})());
});
org.numenta.sanity.demos.hotgym.y__GT_consumption = (function org$numenta$sanity$demos$hotgym$y__GT_consumption(y,h,top,bottom){
return ((((1) - (y / h)) * (top - bottom)) + bottom);
});
org.numenta.sanity.demos.hotgym.consumption__GT_y = (function org$numenta$sanity$demos$hotgym$consumption__GT_y(consumption,top,unit_height){
return ((top - consumption) * unit_height);
});
org.numenta.sanity.demos.hotgym.anomaly_radar_pane = (function org$numenta$sanity$demos$hotgym$anomaly_radar_pane(){
var step__GT_scores = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.PersistentArrayMap.EMPTY);
var hover_i = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
var hover_y = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.main.steps,cljs.core.cst$kw$org$numenta$sanity$demos$hotgym_SLASH_fetch_DASH_anomaly_DASH_radar,((function (step__GT_scores,hover_i,hover_y){
return (function (_,___$1,___$2,steps_v){
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(step__GT_scores,cljs.core.select_keys,steps_v);

var seq__71384 = cljs.core.seq(cljs.core.remove.cljs$core$IFn$_invoke$arity$2(cljs.core.partial.cljs$core$IFn$_invoke$arity$2(cljs.core.contains_QMARK_,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(step__GT_scores) : cljs.core.deref.call(null,step__GT_scores))),steps_v));
var chunk__71386 = null;
var count__71387 = (0);
var i__71388 = (0);
while(true){
if((i__71388 < count__71387)){
var step = chunk__71386.cljs$core$IIndexed$_nth$arity$2(null,i__71388);
var out_c_71598 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var snapshot_id_71599 = cljs.core.cst$kw$snapshot_DASH_id.cljs$core$IFn$_invoke$arity$1(step);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, ["decode-predictive-columns",snapshot_id_71599,cljs.core.cst$kw$power_DASH_consumption,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.n_predictions) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.n_predictions)),org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(out_c_71598,true)], null));

if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.try_boundaries_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.try_boundaries_QMARK_)))){
org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,(-10));

org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,(110));
} else {
}

if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.try_last_value_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.try_last_value_QMARK_)))){
org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(step,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input_DASH_value,cljs.core.cst$kw$consumption], null)));
} else {
}

var c__38109__auto___71600 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71600,out_c_71598,snapshot_id_71599,step,step__GT_scores,hover_i,hover_y){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71600,out_c_71598,snapshot_id_71599,step,step__GT_scores,hover_i,hover_y){
return (function (state_71434){
var state_val_71435 = (state_71434[(1)]);
if((state_val_71435 === (7))){
var inst_71430 = (state_71434[(2)]);
var state_71434__$1 = state_71434;
var statearr_71436_71601 = state_71434__$1;
(statearr_71436_71601[(2)] = inst_71430);

(statearr_71436_71601[(1)] = (4));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (1))){
var state_71434__$1 = state_71434;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71434__$1,(2),out_c_71598);
} else {
if((state_val_71435 === (4))){
var inst_71432 = (state_71434[(2)]);
var state_71434__$1 = state_71434;
return cljs.core.async.impl.ioc_helpers.return_chan(state_71434__$1,inst_71432);
} else {
if((state_val_71435 === (13))){
var inst_71425 = (state_71434[(2)]);
var state_71434__$1 = state_71434;
var statearr_71437_71602 = state_71434__$1;
(statearr_71437_71602[(2)] = inst_71425);

(statearr_71437_71602[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (6))){
var inst_71398 = (state_71434[(7)]);
var inst_71411 = (state_71434[(8)]);
var inst_71411__$1 = cljs.core.seq(inst_71398);
var state_71434__$1 = (function (){var statearr_71438 = state_71434;
(statearr_71438[(8)] = inst_71411__$1);

return statearr_71438;
})();
if(inst_71411__$1){
var statearr_71439_71603 = state_71434__$1;
(statearr_71439_71603[(1)] = (8));

} else {
var statearr_71440_71604 = state_71434__$1;
(statearr_71440_71604[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (3))){
var inst_71400 = (state_71434[(9)]);
var inst_71401 = (state_71434[(10)]);
var inst_71403 = (inst_71401 < inst_71400);
var inst_71404 = inst_71403;
var state_71434__$1 = state_71434;
if(cljs.core.truth_(inst_71404)){
var statearr_71441_71605 = state_71434__$1;
(statearr_71441_71605[(1)] = (5));

} else {
var statearr_71442_71606 = state_71434__$1;
(statearr_71442_71606[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (12))){
var inst_71411 = (state_71434[(8)]);
var inst_71420 = cljs.core.first(inst_71411);
var inst_71421 = org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,inst_71420);
var inst_71422 = cljs.core.next(inst_71411);
var inst_71398 = inst_71422;
var inst_71399 = null;
var inst_71400 = (0);
var inst_71401 = (0);
var state_71434__$1 = (function (){var statearr_71443 = state_71434;
(statearr_71443[(9)] = inst_71400);

(statearr_71443[(10)] = inst_71401);

(statearr_71443[(11)] = inst_71421);

(statearr_71443[(7)] = inst_71398);

(statearr_71443[(12)] = inst_71399);

return statearr_71443;
})();
var statearr_71444_71607 = state_71434__$1;
(statearr_71444_71607[(2)] = null);

(statearr_71444_71607[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (2))){
var inst_71395 = (state_71434[(2)]);
var inst_71396 = cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$value,inst_71395);
var inst_71397 = cljs.core.seq(inst_71396);
var inst_71398 = inst_71397;
var inst_71399 = null;
var inst_71400 = (0);
var inst_71401 = (0);
var state_71434__$1 = (function (){var statearr_71445 = state_71434;
(statearr_71445[(9)] = inst_71400);

(statearr_71445[(10)] = inst_71401);

(statearr_71445[(7)] = inst_71398);

(statearr_71445[(12)] = inst_71399);

return statearr_71445;
})();
var statearr_71446_71608 = state_71434__$1;
(statearr_71446_71608[(2)] = null);

(statearr_71446_71608[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (11))){
var inst_71411 = (state_71434[(8)]);
var inst_71415 = cljs.core.chunk_first(inst_71411);
var inst_71416 = cljs.core.chunk_rest(inst_71411);
var inst_71417 = cljs.core.count(inst_71415);
var inst_71398 = inst_71416;
var inst_71399 = inst_71415;
var inst_71400 = inst_71417;
var inst_71401 = (0);
var state_71434__$1 = (function (){var statearr_71450 = state_71434;
(statearr_71450[(9)] = inst_71400);

(statearr_71450[(10)] = inst_71401);

(statearr_71450[(7)] = inst_71398);

(statearr_71450[(12)] = inst_71399);

return statearr_71450;
})();
var statearr_71451_71609 = state_71434__$1;
(statearr_71451_71609[(2)] = null);

(statearr_71451_71609[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (9))){
var state_71434__$1 = state_71434;
var statearr_71452_71610 = state_71434__$1;
(statearr_71452_71610[(2)] = null);

(statearr_71452_71610[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (5))){
var inst_71400 = (state_71434[(9)]);
var inst_71401 = (state_71434[(10)]);
var inst_71398 = (state_71434[(7)]);
var inst_71399 = (state_71434[(12)]);
var inst_71406 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(inst_71399,inst_71401);
var inst_71407 = org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,inst_71406);
var inst_71408 = (inst_71401 + (1));
var tmp71447 = inst_71400;
var tmp71448 = inst_71398;
var tmp71449 = inst_71399;
var inst_71398__$1 = tmp71448;
var inst_71399__$1 = tmp71449;
var inst_71400__$1 = tmp71447;
var inst_71401__$1 = inst_71408;
var state_71434__$1 = (function (){var statearr_71453 = state_71434;
(statearr_71453[(9)] = inst_71400__$1);

(statearr_71453[(10)] = inst_71401__$1);

(statearr_71453[(13)] = inst_71407);

(statearr_71453[(7)] = inst_71398__$1);

(statearr_71453[(12)] = inst_71399__$1);

return statearr_71453;
})();
var statearr_71454_71611 = state_71434__$1;
(statearr_71454_71611[(2)] = null);

(statearr_71454_71611[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (10))){
var inst_71428 = (state_71434[(2)]);
var state_71434__$1 = state_71434;
var statearr_71455_71612 = state_71434__$1;
(statearr_71455_71612[(2)] = inst_71428);

(statearr_71455_71612[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71435 === (8))){
var inst_71411 = (state_71434[(8)]);
var inst_71413 = cljs.core.chunked_seq_QMARK_(inst_71411);
var state_71434__$1 = state_71434;
if(inst_71413){
var statearr_71456_71613 = state_71434__$1;
(statearr_71456_71613[(1)] = (11));

} else {
var statearr_71457_71614 = state_71434__$1;
(statearr_71457_71614[(1)] = (12));

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
});})(seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71600,out_c_71598,snapshot_id_71599,step,step__GT_scores,hover_i,hover_y))
;
return ((function (seq__71384,chunk__71386,count__71387,i__71388,switch__37995__auto__,c__38109__auto___71600,out_c_71598,snapshot_id_71599,step,step__GT_scores,hover_i,hover_y){
return (function() {
var org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____0 = (function (){
var statearr_71461 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_71461[(0)] = org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__);

(statearr_71461[(1)] = (1));

return statearr_71461;
});
var org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____1 = (function (state_71434){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71434);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71462){if((e71462 instanceof Object)){
var ex__37999__auto__ = e71462;
var statearr_71463_71615 = state_71434;
(statearr_71463_71615[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71434);

return cljs.core.cst$kw$recur;
} else {
throw e71462;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__71616 = state_71434;
state_71434 = G__71616;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__ = function(state_71434){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____1.call(this,state_71434);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__;
})()
;})(seq__71384,chunk__71386,count__71387,i__71388,switch__37995__auto__,c__38109__auto___71600,out_c_71598,snapshot_id_71599,step,step__GT_scores,hover_i,hover_y))
})();
var state__38111__auto__ = (function (){var statearr_71464 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71464[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___71600);

return statearr_71464;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71600,out_c_71598,snapshot_id_71599,step,step__GT_scores,hover_i,hover_y))
);


var G__71617 = seq__71384;
var G__71618 = chunk__71386;
var G__71619 = count__71387;
var G__71620 = (i__71388 + (1));
seq__71384 = G__71617;
chunk__71386 = G__71618;
count__71387 = G__71619;
i__71388 = G__71620;
continue;
} else {
var temp__4657__auto__ = cljs.core.seq(seq__71384);
if(temp__4657__auto__){
var seq__71384__$1 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(seq__71384__$1)){
var c__6956__auto__ = cljs.core.chunk_first(seq__71384__$1);
var G__71621 = cljs.core.chunk_rest(seq__71384__$1);
var G__71622 = c__6956__auto__;
var G__71623 = cljs.core.count(c__6956__auto__);
var G__71624 = (0);
seq__71384 = G__71621;
chunk__71386 = G__71622;
count__71387 = G__71623;
i__71388 = G__71624;
continue;
} else {
var step = cljs.core.first(seq__71384__$1);
var out_c_71625 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var snapshot_id_71626 = cljs.core.cst$kw$snapshot_DASH_id.cljs$core$IFn$_invoke$arity$1(step);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, ["decode-predictive-columns",snapshot_id_71626,cljs.core.cst$kw$power_DASH_consumption,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.n_predictions) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.n_predictions)),org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(out_c_71625,true)], null));

if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.try_boundaries_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.try_boundaries_QMARK_)))){
org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,(-10));

org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,(110));
} else {
}

if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.try_last_value_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.try_last_value_QMARK_)))){
org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(step,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input_DASH_value,cljs.core.cst$kw$consumption], null)));
} else {
}

var c__38109__auto___71627 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71627,out_c_71625,snapshot_id_71626,step,seq__71384__$1,temp__4657__auto__,step__GT_scores,hover_i,hover_y){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71627,out_c_71625,snapshot_id_71626,step,seq__71384__$1,temp__4657__auto__,step__GT_scores,hover_i,hover_y){
return (function (state_71509){
var state_val_71510 = (state_71509[(1)]);
if((state_val_71510 === (7))){
var inst_71505 = (state_71509[(2)]);
var state_71509__$1 = state_71509;
var statearr_71511_71628 = state_71509__$1;
(statearr_71511_71628[(2)] = inst_71505);

(statearr_71511_71628[(1)] = (4));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (1))){
var state_71509__$1 = state_71509;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_71509__$1,(2),out_c_71625);
} else {
if((state_val_71510 === (4))){
var inst_71507 = (state_71509[(2)]);
var state_71509__$1 = state_71509;
return cljs.core.async.impl.ioc_helpers.return_chan(state_71509__$1,inst_71507);
} else {
if((state_val_71510 === (13))){
var inst_71500 = (state_71509[(2)]);
var state_71509__$1 = state_71509;
var statearr_71512_71629 = state_71509__$1;
(statearr_71512_71629[(2)] = inst_71500);

(statearr_71512_71629[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (6))){
var inst_71473 = (state_71509[(7)]);
var inst_71486 = (state_71509[(8)]);
var inst_71486__$1 = cljs.core.seq(inst_71473);
var state_71509__$1 = (function (){var statearr_71513 = state_71509;
(statearr_71513[(8)] = inst_71486__$1);

return statearr_71513;
})();
if(inst_71486__$1){
var statearr_71514_71630 = state_71509__$1;
(statearr_71514_71630[(1)] = (8));

} else {
var statearr_71515_71631 = state_71509__$1;
(statearr_71515_71631[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (3))){
var inst_71476 = (state_71509[(9)]);
var inst_71475 = (state_71509[(10)]);
var inst_71478 = (inst_71476 < inst_71475);
var inst_71479 = inst_71478;
var state_71509__$1 = state_71509;
if(cljs.core.truth_(inst_71479)){
var statearr_71516_71632 = state_71509__$1;
(statearr_71516_71632[(1)] = (5));

} else {
var statearr_71517_71633 = state_71509__$1;
(statearr_71517_71633[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (12))){
var inst_71486 = (state_71509[(8)]);
var inst_71495 = cljs.core.first(inst_71486);
var inst_71496 = org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,inst_71495);
var inst_71497 = cljs.core.next(inst_71486);
var inst_71473 = inst_71497;
var inst_71474 = null;
var inst_71475 = (0);
var inst_71476 = (0);
var state_71509__$1 = (function (){var statearr_71518 = state_71509;
(statearr_71518[(7)] = inst_71473);

(statearr_71518[(9)] = inst_71476);

(statearr_71518[(11)] = inst_71496);

(statearr_71518[(12)] = inst_71474);

(statearr_71518[(10)] = inst_71475);

return statearr_71518;
})();
var statearr_71519_71634 = state_71509__$1;
(statearr_71519_71634[(2)] = null);

(statearr_71519_71634[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (2))){
var inst_71470 = (state_71509[(2)]);
var inst_71471 = cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$value,inst_71470);
var inst_71472 = cljs.core.seq(inst_71471);
var inst_71473 = inst_71472;
var inst_71474 = null;
var inst_71475 = (0);
var inst_71476 = (0);
var state_71509__$1 = (function (){var statearr_71520 = state_71509;
(statearr_71520[(7)] = inst_71473);

(statearr_71520[(9)] = inst_71476);

(statearr_71520[(12)] = inst_71474);

(statearr_71520[(10)] = inst_71475);

return statearr_71520;
})();
var statearr_71521_71635 = state_71509__$1;
(statearr_71521_71635[(2)] = null);

(statearr_71521_71635[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (11))){
var inst_71486 = (state_71509[(8)]);
var inst_71490 = cljs.core.chunk_first(inst_71486);
var inst_71491 = cljs.core.chunk_rest(inst_71486);
var inst_71492 = cljs.core.count(inst_71490);
var inst_71473 = inst_71491;
var inst_71474 = inst_71490;
var inst_71475 = inst_71492;
var inst_71476 = (0);
var state_71509__$1 = (function (){var statearr_71525 = state_71509;
(statearr_71525[(7)] = inst_71473);

(statearr_71525[(9)] = inst_71476);

(statearr_71525[(12)] = inst_71474);

(statearr_71525[(10)] = inst_71475);

return statearr_71525;
})();
var statearr_71526_71636 = state_71509__$1;
(statearr_71526_71636[(2)] = null);

(statearr_71526_71636[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (9))){
var state_71509__$1 = state_71509;
var statearr_71527_71637 = state_71509__$1;
(statearr_71527_71637[(2)] = null);

(statearr_71527_71637[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (5))){
var inst_71473 = (state_71509[(7)]);
var inst_71476 = (state_71509[(9)]);
var inst_71474 = (state_71509[(12)]);
var inst_71475 = (state_71509[(10)]);
var inst_71481 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(inst_71474,inst_71476);
var inst_71482 = org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,step,inst_71481);
var inst_71483 = (inst_71476 + (1));
var tmp71522 = inst_71473;
var tmp71523 = inst_71474;
var tmp71524 = inst_71475;
var inst_71473__$1 = tmp71522;
var inst_71474__$1 = tmp71523;
var inst_71475__$1 = tmp71524;
var inst_71476__$1 = inst_71483;
var state_71509__$1 = (function (){var statearr_71528 = state_71509;
(statearr_71528[(7)] = inst_71473__$1);

(statearr_71528[(9)] = inst_71476__$1);

(statearr_71528[(12)] = inst_71474__$1);

(statearr_71528[(13)] = inst_71482);

(statearr_71528[(10)] = inst_71475__$1);

return statearr_71528;
})();
var statearr_71529_71638 = state_71509__$1;
(statearr_71529_71638[(2)] = null);

(statearr_71529_71638[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (10))){
var inst_71503 = (state_71509[(2)]);
var state_71509__$1 = state_71509;
var statearr_71530_71639 = state_71509__$1;
(statearr_71530_71639[(2)] = inst_71503);

(statearr_71530_71639[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_71510 === (8))){
var inst_71486 = (state_71509[(8)]);
var inst_71488 = cljs.core.chunked_seq_QMARK_(inst_71486);
var state_71509__$1 = state_71509;
if(inst_71488){
var statearr_71531_71640 = state_71509__$1;
(statearr_71531_71640[(1)] = (11));

} else {
var statearr_71532_71641 = state_71509__$1;
(statearr_71532_71641[(1)] = (12));

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
});})(seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71627,out_c_71625,snapshot_id_71626,step,seq__71384__$1,temp__4657__auto__,step__GT_scores,hover_i,hover_y))
;
return ((function (seq__71384,chunk__71386,count__71387,i__71388,switch__37995__auto__,c__38109__auto___71627,out_c_71625,snapshot_id_71626,step,seq__71384__$1,temp__4657__auto__,step__GT_scores,hover_i,hover_y){
return (function() {
var org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____0 = (function (){
var statearr_71536 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_71536[(0)] = org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__);

(statearr_71536[(1)] = (1));

return statearr_71536;
});
var org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____1 = (function (state_71509){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_71509);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e71537){if((e71537 instanceof Object)){
var ex__37999__auto__ = e71537;
var statearr_71538_71642 = state_71509;
(statearr_71538_71642[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_71509);

return cljs.core.cst$kw$recur;
} else {
throw e71537;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__71643 = state_71509;
state_71509 = G__71643;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__ = function(state_71509){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____1.call(this,state_71509);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_state_machine__37996__auto__;
})()
;})(seq__71384,chunk__71386,count__71387,i__71388,switch__37995__auto__,c__38109__auto___71627,out_c_71625,snapshot_id_71626,step,seq__71384__$1,temp__4657__auto__,step__GT_scores,hover_i,hover_y))
})();
var state__38111__auto__ = (function (){var statearr_71539 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_71539[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___71627);

return statearr_71539;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(seq__71384,chunk__71386,count__71387,i__71388,c__38109__auto___71627,out_c_71625,snapshot_id_71626,step,seq__71384__$1,temp__4657__auto__,step__GT_scores,hover_i,hover_y))
);


var G__71644 = cljs.core.next(seq__71384__$1);
var G__71645 = null;
var G__71646 = (0);
var G__71647 = (0);
seq__71384 = G__71644;
chunk__71386 = G__71645;
count__71387 = G__71646;
i__71388 = G__71647;
continue;
}
} else {
return null;
}
}
break;
}
});})(step__GT_scores,hover_i,hover_y))
);

return ((function (step__GT_scores,hover_i,hover_y){
return (function (){
var h = (400);
var draw_steps = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.viz_options) : cljs.core.deref.call(null,org.numenta.sanity.main.viz_options)),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$drawing,cljs.core.cst$kw$draw_DASH_steps], null));
var w = (org.numenta.sanity.demos.hotgym.unit_width * draw_steps);
var h_pad_top = (15);
var h_pad_bottom = (8);
var w_pad_left = (20);
var w_pad_right = (42);
var top = (110);
var bottom = (-10);
var unit_height = (h / (top - bottom));
var label_every = (10);
var center_dt = cljs.core.cst$kw$dt.cljs$core$IFn$_invoke$arity$1(cljs.core.peek((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.selection) : cljs.core.deref.call(null,org.numenta.sanity.main.selection))));
var dt0 = (function (){var x__6484__auto__ = (-1);
var y__6485__auto__ = (center_dt - cljs.core.quot(draw_steps,(2)));
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})();
var center_i = (center_dt - dt0);
var draw_dts = cljs.core.range.cljs$core$IFn$_invoke$arity$2(dt0,(function (){var x__6491__auto__ = (dt0 + draw_steps);
var y__6492__auto__ = cljs.core.count((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps)));
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})());
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$position,"relative",cljs.core.cst$kw$width,((w_pad_left + w) + w_pad_right)], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$position,"absolute",cljs.core.cst$kw$top,(0),cljs.core.cst$kw$left,(0),cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$font_DASH_weight,"bold"], null)], null),"power-consumption"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$svg,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$height,((h + h_pad_top) + h_pad_bottom),cljs.core.cst$kw$width,((w + w_pad_left) + w_pad_right)], null),new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$transform,[cljs.core.str("translate("),cljs.core.str(w_pad_left),cljs.core.str(","),cljs.core.str(h_pad_top),cljs.core.str(")")].join('')], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.consumption_axis_svg,h,bottom,top], null),cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g], null),(function (){var iter__6925__auto__ = ((function (h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540(s__71541){
return (new cljs.core.LazySeq(null,((function (h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (){
var s__71541__$1 = s__71541;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__71541__$1);
if(temp__4657__auto__){
var s__71541__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__71541__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71541__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71543 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71542 = (0);
while(true){
if((i__71542 < size__6924__auto__)){
var i = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71542);
var dt = cljs.core.nth.cljs$core$IFn$_invoke$arity$2(draw_dts,i);
var from_step = cljs.core.nth.cljs$core$IFn$_invoke$arity$3((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps)),(dt + (1)),null);
var y_scores = (cljs.core.truth_(from_step)?(function (){var iter__6925__auto__ = ((function (i__71542,dt,from_step,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540_$_iter__71568(s__71569){
return (new cljs.core.LazySeq(null,((function (i__71542,dt,from_step,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (){
var s__71569__$1 = s__71569;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__71569__$1);
if(temp__4657__auto____$1){
var s__71569__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__71569__$2)){
var c__6923__auto____$1 = cljs.core.chunk_first(s__71569__$2);
var size__6924__auto____$1 = cljs.core.count(c__6923__auto____$1);
var b__71571 = cljs.core.chunk_buffer(size__6924__auto____$1);
if((function (){var i__71570 = (0);
while(true){
if((i__71570 < size__6924__auto____$1)){
var vec__71576 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto____$1,i__71570);
var consumption = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71576,(0),null);
var score = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71576,(1),null);
cljs.core.chunk_append(b__71571,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.consumption__GT_y(consumption,top,unit_height),score], null));

var G__71648 = (i__71570 + (1));
i__71570 = G__71648;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71571),org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540_$_iter__71568(cljs.core.chunk_rest(s__71569__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71571),null);
}
} else {
var vec__71577 = cljs.core.first(s__71569__$2);
var consumption = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71577,(0),null);
var score = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71577,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.consumption__GT_y(consumption,top,unit_height),score], null),org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540_$_iter__71568(cljs.core.rest(s__71569__$2)));
}
} else {
return null;
}
break;
}
});})(i__71542,dt,from_step,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,null,null));
});})(i__71542,dt,from_step,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
;
return iter__6925__auto__(cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.first,cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(step__GT_scores) : cljs.core.deref.call(null,step__GT_scores)),from_step)));
})():null);
cljs.core.chunk_append(b__71543,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$transform,[cljs.core.str("translate("),cljs.core.str((org.numenta.sanity.demos.hotgym.unit_width * ((draw_steps - (1)) - i))),cljs.core.str(",0)")].join('')], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rect,(function (){var G__71578 = new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$width,org.numenta.sanity.demos.hotgym.unit_width,cljs.core.cst$kw$height,h,cljs.core.cst$kw$fill,"white"], null);
if(cljs.core.truth_(from_step)){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(G__71578,cljs.core.cst$kw$on_DASH_click,((function (i__71542,G__71578,dt,from_step,y_scores,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (e){
var y = (e.clientY - e.target.getBoundingClientRect().top);
return org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,from_step,org.numenta.sanity.demos.hotgym.y__GT_consumption(y,h,top,bottom));
});})(i__71542,G__71578,dt,from_step,y_scores,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,cljs.core.array_seq([cljs.core.cst$kw$on_DASH_mouse_DASH_move,((function (i__71542,G__71578,dt,from_step,y_scores,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (e){
var y = (e.clientY - e.target.getBoundingClientRect().top);
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_i,i) : cljs.core.reset_BANG_.call(null,hover_i,i));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_y,y) : cljs.core.reset_BANG_.call(null,hover_y,y));
});})(i__71542,G__71578,dt,from_step,y_scores,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,cljs.core.cst$kw$on_DASH_mouse_DASH_leave,((function (i__71542,G__71578,dt,from_step,y_scores,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (e){
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_i,null) : cljs.core.reset_BANG_.call(null,hover_i,null));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_y,null) : cljs.core.reset_BANG_.call(null,hover_y,null));
});})(i__71542,G__71578,dt,from_step,y_scores,i,c__6923__auto__,size__6924__auto__,b__71543,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
], 0));
} else {
return G__71578;
}
})()], null),new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$pointer_DASH_events,"none"], null)], null),(cljs.core.truth_(cljs.core.not_empty(y_scores))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.anomaly_gradient_svg,y_scores], null):null),(cljs.core.truth_(cljs.core.not_empty(y_scores))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.anomaly_samples_svg,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.first,y_scores)], null):null),(((((0) <= dt)) && ((dt < cljs.core.count((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps))))))?new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.actual_svg,cljs.core.nth.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps)),dt),top,unit_height], null):null),(cljs.core.truth_(cljs.core.not_empty(y_scores))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.prediction_svg,y_scores], null):null)], null)], null));

var G__71649 = (i__71542 + (1));
i__71542 = G__71649;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71543),org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540(cljs.core.chunk_rest(s__71541__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71543),null);
}
} else {
var i = cljs.core.first(s__71541__$2);
var dt = cljs.core.nth.cljs$core$IFn$_invoke$arity$2(draw_dts,i);
var from_step = cljs.core.nth.cljs$core$IFn$_invoke$arity$3((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps)),(dt + (1)),null);
var y_scores = (cljs.core.truth_(from_step)?(function (){var iter__6925__auto__ = ((function (dt,from_step,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540_$_iter__71579(s__71580){
return (new cljs.core.LazySeq(null,((function (dt,from_step,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (){
var s__71580__$1 = s__71580;
while(true){
var temp__4657__auto____$1 = cljs.core.seq(s__71580__$1);
if(temp__4657__auto____$1){
var s__71580__$2 = temp__4657__auto____$1;
if(cljs.core.chunked_seq_QMARK_(s__71580__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71580__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71582 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71581 = (0);
while(true){
if((i__71581 < size__6924__auto__)){
var vec__71587 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71581);
var consumption = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71587,(0),null);
var score = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71587,(1),null);
cljs.core.chunk_append(b__71582,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.consumption__GT_y(consumption,top,unit_height),score], null));

var G__71650 = (i__71581 + (1));
i__71581 = G__71650;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71582),org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540_$_iter__71579(cljs.core.chunk_rest(s__71580__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71582),null);
}
} else {
var vec__71588 = cljs.core.first(s__71580__$2);
var consumption = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71588,(0),null);
var score = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71588,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.consumption__GT_y(consumption,top,unit_height),score], null),org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540_$_iter__71579(cljs.core.rest(s__71580__$2)));
}
} else {
return null;
}
break;
}
});})(dt,from_step,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,null,null));
});})(dt,from_step,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
;
return iter__6925__auto__(cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.first,cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(step__GT_scores) : cljs.core.deref.call(null,step__GT_scores)),from_step)));
})():null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$transform,[cljs.core.str("translate("),cljs.core.str((org.numenta.sanity.demos.hotgym.unit_width * ((draw_steps - (1)) - i))),cljs.core.str(",0)")].join('')], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rect,(function (){var G__71589 = new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$width,org.numenta.sanity.demos.hotgym.unit_width,cljs.core.cst$kw$height,h,cljs.core.cst$kw$fill,"white"], null);
if(cljs.core.truth_(from_step)){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(G__71589,cljs.core.cst$kw$on_DASH_click,((function (G__71589,dt,from_step,y_scores,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (e){
var y = (e.clientY - e.target.getBoundingClientRect().top);
return org.numenta.sanity.demos.hotgym.consider_consumption_BANG_(step__GT_scores,from_step,org.numenta.sanity.demos.hotgym.y__GT_consumption(y,h,top,bottom));
});})(G__71589,dt,from_step,y_scores,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,cljs.core.array_seq([cljs.core.cst$kw$on_DASH_mouse_DASH_move,((function (G__71589,dt,from_step,y_scores,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (e){
var y = (e.clientY - e.target.getBoundingClientRect().top);
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_i,i) : cljs.core.reset_BANG_.call(null,hover_i,i));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_y,y) : cljs.core.reset_BANG_.call(null,hover_y,y));
});})(G__71589,dt,from_step,y_scores,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,cljs.core.cst$kw$on_DASH_mouse_DASH_leave,((function (G__71589,dt,from_step,y_scores,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (e){
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_i,null) : cljs.core.reset_BANG_.call(null,hover_i,null));

return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(hover_y,null) : cljs.core.reset_BANG_.call(null,hover_y,null));
});})(G__71589,dt,from_step,y_scores,i,s__71541__$2,temp__4657__auto__,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
], 0));
} else {
return G__71589;
}
})()], null),new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$pointer_DASH_events,"none"], null)], null),(cljs.core.truth_(cljs.core.not_empty(y_scores))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.anomaly_gradient_svg,y_scores], null):null),(cljs.core.truth_(cljs.core.not_empty(y_scores))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.anomaly_samples_svg,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.first,y_scores)], null):null),(((((0) <= dt)) && ((dt < cljs.core.count((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps))))))?new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.actual_svg,cljs.core.nth.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps)),dt),top,unit_height], null):null),(cljs.core.truth_(cljs.core.not_empty(y_scores))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.prediction_svg,y_scores], null):null)], null)], null),org$numenta$sanity$demos$hotgym$anomaly_radar_pane_$_iter__71540(cljs.core.rest(s__71541__$2)));
}
} else {
return null;
}
break;
}
});})(h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,null,null));
});})(h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
;
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1(cljs.core.count(draw_dts)));
})()),(function (){var x = (org.numenta.sanity.demos.hotgym.unit_width * ((draw_steps - (1)) - center_i));
var points = [cljs.core.str(x),cljs.core.str(","),cljs.core.str((0)),cljs.core.str(" "),cljs.core.str(x),cljs.core.str(","),cljs.core.str((-1)),cljs.core.str(" "),cljs.core.str((x + org.numenta.sanity.demos.hotgym.unit_width)),cljs.core.str(","),cljs.core.str((-1)),cljs.core.str(" "),cljs.core.str((x + org.numenta.sanity.demos.hotgym.unit_width)),cljs.core.str(","),cljs.core.str((0))].join('');
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,(function (){var points__$1 = [cljs.core.str(x),cljs.core.str(","),cljs.core.str((0)),cljs.core.str(" "),cljs.core.str(x),cljs.core.str(","),cljs.core.str((-1)),cljs.core.str(" "),cljs.core.str((x + org.numenta.sanity.demos.hotgym.unit_width)),cljs.core.str(","),cljs.core.str((-1)),cljs.core.str(" "),cljs.core.str((x + org.numenta.sanity.demos.hotgym.unit_width)),cljs.core.str(","),cljs.core.str((0))].join('');
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$polyline,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$stroke,cljs.core.cst$kw$highlight.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.viz_canvas.state_colors),cljs.core.cst$kw$stroke_DASH_width,(3),cljs.core.cst$kw$fill,"none",cljs.core.cst$kw$points,points__$1], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$polyline,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$stroke,"black",cljs.core.cst$kw$stroke_DASH_width,0.75,cljs.core.cst$kw$fill,"none",cljs.core.cst$kw$points,points__$1], null)], null)], null);
})(),(function (){var points__$1 = [cljs.core.str(x),cljs.core.str(","),cljs.core.str(h),cljs.core.str(" "),cljs.core.str(x),cljs.core.str(","),cljs.core.str((h + (6))),cljs.core.str(" "),cljs.core.str((x + org.numenta.sanity.demos.hotgym.unit_width)),cljs.core.str(","),cljs.core.str((h + (6))),cljs.core.str(" "),cljs.core.str((x + org.numenta.sanity.demos.hotgym.unit_width)),cljs.core.str(","),cljs.core.str(h)].join('');
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$g,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$polyline,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$stroke,cljs.core.cst$kw$highlight.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.viz_canvas.state_colors),cljs.core.cst$kw$stroke_DASH_width,(3),cljs.core.cst$kw$fill,"none",cljs.core.cst$kw$points,points__$1], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$polyline,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$stroke,"black",cljs.core.cst$kw$stroke_DASH_width,0.75,cljs.core.cst$kw$fill,"none",cljs.core.cst$kw$points,points__$1], null)], null)], null);
})()], null);
})()], null)], null),(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(hover_y) : cljs.core.deref.call(null,hover_y)))?(function (){var i = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(hover_i) : cljs.core.deref.call(null,hover_i));
var dt = cljs.core.nth.cljs$core$IFn$_invoke$arity$2(draw_dts,i);
var from_step = cljs.core.nth.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps)),(dt + (1)));
var y = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(hover_y) : cljs.core.deref.call(null,hover_y));
var consumption = org.numenta.sanity.demos.hotgym.y__GT_consumption(y,h,top,bottom);
var vec__71590 = cljs.core.first(cljs.core.filter.cljs$core$IFn$_invoke$arity$2(((function (i,dt,from_step,y,consumption,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y){
return (function (p__71593){
var vec__71594 = p__71593;
var vec__71595 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71594,(0),null);
var c1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71595,(0),null);
var s1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71595,(1),null);
var vec__71596 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71594,(1),null);
var c2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71596,(0),null);
var s2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71596,(1),null);
return ((c1 <= consumption)) && ((consumption <= c2));
});})(i,dt,from_step,y,consumption,h,draw_steps,w,h_pad_top,h_pad_bottom,w_pad_left,w_pad_right,top,bottom,unit_height,label_every,center_dt,dt0,center_i,draw_dts,step__GT_scores,hover_i,hover_y))
,cljs.core.partition.cljs$core$IFn$_invoke$arity$3((2),(1),cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(cljs.core.first,cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(step__GT_scores) : cljs.core.deref.call(null,step__GT_scores)),from_step)))));
var vec__71591 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71590,(0),null);
var lower_consumption = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71591,(0),null);
var lower_score = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71591,(1),null);
var vec__71592 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71590,(1),null);
var upper_consumption = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71592,(0),null);
var upper_score = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71592,(1),null);
var lower_y = org.numenta.sanity.demos.hotgym.consumption__GT_y(lower_consumption,top,unit_height);
var upper_y = org.numenta.sanity.demos.hotgym.consumption__GT_y(upper_consumption,top,unit_height);
var dt_left = (w_pad_left + (org.numenta.sanity.demos.hotgym.unit_width * (((draw_steps - (1)) - i) + 0.5)));
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$position,"absolute",cljs.core.cst$kw$left,(0),cljs.core.cst$kw$top,h_pad_top,cljs.core.cst$kw$pointer_DASH_events,"none"], null)], null),new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.horizontal_label,dt_left,lower_y,(w + w_pad_left),true,null,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,[cljs.core.str(lower_consumption.toFixed((1))),cljs.core.str("kW")].join(''),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),[cljs.core.str(lower_score.toFixed((3)))].join('')], null)], null),(function (){var contents = new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,[cljs.core.str(consumption.toFixed((1))),cljs.core.str("kW")].join(''),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),"click"], null);
var vec__71597 = ((((y - upper_y) > (30)))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [contents,null], null):((((lower_y - y) > (30)))?new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [null,contents], null):new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [null,null], null)
));
var above = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71597,(0),null);
var below = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71597,(1),null);
return new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.horizontal_label,dt_left,y,(w + w_pad_left),false,above,below], null);
})(),new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.horizontal_label,dt_left,upper_y,(w + w_pad_left),true,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,[cljs.core.str(upper_consumption.toFixed((1))),cljs.core.str("kW")].join(''),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),[cljs.core.str(upper_score.toFixed((3)))].join('')], null),null], null)], null);
})():null)], null);
});
;})(step__GT_scores,hover_i,hover_y))
});
org.numenta.sanity.demos.hotgym.world_pane = (function org$numenta$sanity$demos$hotgym$world_pane(){
if(cljs.core.truth_(cljs.core.not_empty((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.steps) : cljs.core.deref.call(null,org.numenta.sanity.main.steps))))){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$margin_DASH_top,(10)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.anomaly_radar_pane], null)], null)], null),cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$margin_DASH_top,(30)], null)], null),(function (){var iter__6925__auto__ = (function org$numenta$sanity$demos$hotgym$world_pane_$_iter__71661(s__71662){
return (new cljs.core.LazySeq(null,(function (){
var s__71662__$1 = s__71662;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__71662__$1);
if(temp__4657__auto__){
var s__71662__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__71662__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__71662__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__71664 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__71663 = (0);
while(true){
if((i__71663 < size__6924__auto__)){
var vec__71669 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__71663);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71669,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71669,(1),null);
cljs.core.chunk_append(b__71664,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$margin_DASH_bottom,(20)], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$font_DASH_weight,"bold"], null)], null),cljs.core.name(sense_id)], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$strong,[cljs.core.str(v)].join('')], null)], null)], null));

var G__71671 = (i__71663 + (1));
i__71663 = G__71671;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__71664),org$numenta$sanity$demos$hotgym$world_pane_$_iter__71661(cljs.core.chunk_rest(s__71662__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__71664),null);
}
} else {
var vec__71670 = cljs.core.first(s__71662__$2);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71670,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__71670,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$margin_DASH_bottom,(20)], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$font_DASH_weight,"bold"], null)], null),cljs.core.name(sense_id)], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$strong,[cljs.core.str(v)].join('')], null)], null)], null),org$numenta$sanity$demos$hotgym$world_pane_$_iter__71661(cljs.core.rest(s__71662__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$sensed_DASH_values.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0()),cljs.core.cst$kw$power_DASH_consumption));
})())], null);
} else {
return null;
}
});
org.numenta.sanity.demos.hotgym.set_model_BANG_ = (function org$numenta$sanity$demos$hotgym$set_model_BANG_(){
return org.numenta.sanity.helpers.with_ui_loading_message((function (){
var init_QMARK_ = ((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.model)) == null);
var G__71680_71688 = org.numenta.sanity.demos.hotgym.model;
var G__71681_71689 = org.nfrac.comportex.core.region_network(new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$rgn_DASH_0,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$power_DASH_consumption,cljs.core.cst$kw$is_DASH_weekend_QMARK_,cljs.core.cst$kw$hour_DASH_of_DASH_day], null)], null),cljs.core.constantly(org.nfrac.comportex.core.sensory_region),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$rgn_DASH_0,cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(org.nfrac.comportex.cells.better_parameter_defaults,cljs.core.cst$kw$depth,(1),cljs.core.array_seq([cljs.core.cst$kw$max_DASH_segments,(128),cljs.core.cst$kw$distal_DASH_perm_DASH_connected,0.2,cljs.core.cst$kw$distal_DASH_perm_DASH_init,0.2], 0))], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$power_DASH_consumption,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$consumption,org.numenta.sanity.demos.hotgym.sampling_linear_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [((1024) + (256))], null),(17),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [-12.8,112.8], null),12.8)], null)], null),new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$is_DASH_weekend_QMARK_,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$is_DASH_weekend_QMARK_,org.nfrac.comportex.encoders.category_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(10)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [true,false], null))], null),cljs.core.cst$kw$hour_DASH_of_DASH_day,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$hour_DASH_of_DASH_day,org.nfrac.comportex.encoders.category_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [((40) * (24))], null),cljs.core.range.cljs$core$IFn$_invoke$arity$1((24)))], null)], null));
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__71680_71688,G__71681_71689) : cljs.core.reset_BANG_.call(null,G__71680_71688,G__71681_71689));

if(init_QMARK_){
var G__71683_71690 = "../data/hotgym.consumption_weekend_hour.edn";
var G__71684_71691 = ((function (G__71683_71690,init_QMARK_){
return (function (e){
if(cljs.core.truth_(e.target.isSuccess())){
var response = e.target.getResponseText();
var inputs = cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.partial.cljs$core$IFn$_invoke$arity$2(cljs.core.zipmap,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$consumption,cljs.core.cst$kw$is_DASH_weekend_QMARK_,cljs.core.cst$kw$hour_DASH_of_DASH_day], null)),cljs.reader.read_string(response));
return cljs.core.async.onto_chan.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.demos.hotgym.world_c,inputs,false);
} else {
var G__71685 = [cljs.core.str("Request to "),cljs.core.str(e.target.getLastUri()),cljs.core.str(" failed. "),cljs.core.str(e.target.getStatus()),cljs.core.str(" - "),cljs.core.str(e.target.getStatusText())].join('');
return log.error(G__71685);
}
});})(G__71683_71690,init_QMARK_))
;
goog.net.XhrIo.send(G__71683_71690,G__71684_71691);

return org.numenta.sanity.bridge.browser.init.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.hotgym.model,org.numenta.sanity.demos.hotgym.world_c,org.numenta.sanity.main.into_journal,org.numenta.sanity.demos.hotgym.into_sim);
} else {
var G__71686 = org.numenta.sanity.main.network_shape;
var G__71687 = org.numenta.sanity.util.translate_network_shape(org.numenta.sanity.comportex.data.network_shape((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.hotgym.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.hotgym.model))));
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__71686,G__71687) : cljs.core.reset_BANG_.call(null,G__71686,G__71687));
}
}));
});
org.numenta.sanity.demos.hotgym.model_tab = (function org$numenta$sanity$demos$hotgym$model_tab(){
return new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"Numenta's \"hotgym\" dataset."], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"Uses the solution from:",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$a,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$href,"http://mrcslws.com/gorilla/?path=hotgym.clj"], null),"Predicting power consumptions with HTM"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"This demo highlights the Anomaly Radar display on the left. The anomaly\n   scores for possible next inputs are sampled, and the sample points are shown\n   as dots. The prediction is a blue dash, and the actual value is a black\n   dash. The red->white scale represents the anomaly score. The anomaly score is\n   correct wherever there's a dot, and it's estimated elsewhere."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"Inspect the numbers by hovering your mouse over the Anomaly Radar. Click\n   to add your own samples. You might want to pause the simulation first."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"This demo chooses samples by decoding the predictive columns, as\n   explained in the essay above."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"It's fun to click the black dashes and see if it changes the\n   prediction. When this happens, it shows that the HTM actually predicted\n   something better than we thought, we just didn't sample the right points. You\n   could expand on this demo to try different strategies for choosing a clever\n   set of samples, finding the right balance between results and code\n   performance."], null)], null);
});
org.numenta.sanity.demos.hotgym.init = (function org$numenta$sanity$demos$hotgym$init(){
reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,"Comportex",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.model_tab], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.hotgym.world_pane], null),reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$model),org.numenta.sanity.demos.comportex_common.all_features,org.numenta.sanity.demos.hotgym.into_sim], null),goog.dom.getElement("sanity-app"));

return org.numenta.sanity.demos.hotgym.set_model_BANG_();
});
goog.exportSymbol('org.numenta.sanity.demos.hotgym.init', org.numenta.sanity.demos.hotgym.init);
