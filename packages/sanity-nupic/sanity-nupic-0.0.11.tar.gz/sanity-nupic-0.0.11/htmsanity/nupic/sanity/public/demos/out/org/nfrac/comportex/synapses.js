// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.synapses');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.util');

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.nfrac.comportex.synapses.SegUpdate = (function (target_id,operation,grow_sources,die_sources,__meta,__extmap,__hash){
this.target_id = target_id;
this.operation = operation;
this.grow_sources = grow_sources;
this.die_sources = die_sources;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36402,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36404 = (((k36402 instanceof cljs.core.Keyword))?k36402.fqn:null);
switch (G__36404) {
case "target-id":
return self__.target_id;

break;
case "operation":
return self__.operation;

break;
case "grow-sources":
return self__.grow_sources;

break;
case "die-sources":
return self__.die_sources;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36402,else__6770__auto__);

}
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.synapses.SegUpdate{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$target_DASH_id,self__.target_id],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$operation,self__.operation],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$grow_DASH_sources,self__.grow_sources],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$die_DASH_sources,self__.die_sources],null))], null),self__.__extmap));
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36401){
var self__ = this;
var G__36401__$1 = this;
return (new cljs.core.RecordIter((0),G__36401__$1,4,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$target_DASH_id,cljs.core.cst$kw$operation,cljs.core.cst$kw$grow_DASH_sources,cljs.core.cst$kw$die_DASH_sources], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.synapses.SegUpdate(self__.target_id,self__.operation,self__.grow_sources,self__.die_sources,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (4 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$die_DASH_sources,null,cljs.core.cst$kw$operation,null,cljs.core.cst$kw$target_DASH_id,null,cljs.core.cst$kw$grow_DASH_sources,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.synapses.SegUpdate(self__.target_id,self__.operation,self__.grow_sources,self__.die_sources,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36401){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36405 = cljs.core.keyword_identical_QMARK_;
var expr__36406 = k__6775__auto__;
if(cljs.core.truth_((pred__36405.cljs$core$IFn$_invoke$arity$2 ? pred__36405.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$target_DASH_id,expr__36406) : pred__36405.call(null,cljs.core.cst$kw$target_DASH_id,expr__36406)))){
return (new org.nfrac.comportex.synapses.SegUpdate(G__36401,self__.operation,self__.grow_sources,self__.die_sources,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36405.cljs$core$IFn$_invoke$arity$2 ? pred__36405.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$operation,expr__36406) : pred__36405.call(null,cljs.core.cst$kw$operation,expr__36406)))){
return (new org.nfrac.comportex.synapses.SegUpdate(self__.target_id,G__36401,self__.grow_sources,self__.die_sources,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36405.cljs$core$IFn$_invoke$arity$2 ? pred__36405.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$grow_DASH_sources,expr__36406) : pred__36405.call(null,cljs.core.cst$kw$grow_DASH_sources,expr__36406)))){
return (new org.nfrac.comportex.synapses.SegUpdate(self__.target_id,self__.operation,G__36401,self__.die_sources,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36405.cljs$core$IFn$_invoke$arity$2 ? pred__36405.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$die_DASH_sources,expr__36406) : pred__36405.call(null,cljs.core.cst$kw$die_DASH_sources,expr__36406)))){
return (new org.nfrac.comportex.synapses.SegUpdate(self__.target_id,self__.operation,self__.grow_sources,G__36401,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.synapses.SegUpdate(self__.target_id,self__.operation,self__.grow_sources,self__.die_sources,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36401),null));
}
}
}
}
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$target_DASH_id,self__.target_id],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$operation,self__.operation],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$grow_DASH_sources,self__.grow_sources],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$die_DASH_sources,self__.die_sources],null))], null),self__.__extmap));
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36401){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.synapses.SegUpdate(self__.target_id,self__.operation,self__.grow_sources,self__.die_sources,G__36401,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.synapses.SegUpdate.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.synapses.SegUpdate.getBasis = (function (){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$target_DASH_id,cljs.core.cst$sym$operation,cljs.core.cst$sym$grow_DASH_sources,cljs.core.cst$sym$die_DASH_sources], null);
});

org.nfrac.comportex.synapses.SegUpdate.cljs$lang$type = true;

org.nfrac.comportex.synapses.SegUpdate.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.synapses/SegUpdate");
});

org.nfrac.comportex.synapses.SegUpdate.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.synapses/SegUpdate");
});

org.nfrac.comportex.synapses.__GT_SegUpdate = (function org$nfrac$comportex$synapses$__GT_SegUpdate(target_id,operation,grow_sources,die_sources){
return (new org.nfrac.comportex.synapses.SegUpdate(target_id,operation,grow_sources,die_sources,null,null,null));
});

org.nfrac.comportex.synapses.map__GT_SegUpdate = (function org$nfrac$comportex$synapses$map__GT_SegUpdate(G__36403){
return (new org.nfrac.comportex.synapses.SegUpdate(cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(G__36403),cljs.core.cst$kw$operation.cljs$core$IFn$_invoke$arity$1(G__36403),cljs.core.cst$kw$grow_DASH_sources.cljs$core$IFn$_invoke$arity$1(G__36403),cljs.core.cst$kw$die_DASH_sources.cljs$core$IFn$_invoke$arity$1(G__36403),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36403,cljs.core.cst$kw$target_DASH_id,cljs.core.array_seq([cljs.core.cst$kw$operation,cljs.core.cst$kw$grow_DASH_sources,cljs.core.cst$kw$die_DASH_sources], 0)),null));
});

/**
 * Creates a record defining changes to make to a synaptic
 *   segment. Operation can be one of `:learn` (increment active sources,
 *   decrement inactive), `:punish` (decrement active sources) or
 *   `:reinforce` (increment active sources). Without the operation
 *   argument, only the growth and death of synapses will be applied.
 */
org.nfrac.comportex.synapses.seg_update = (function org$nfrac$comportex$synapses$seg_update(var_args){
var args36409 = [];
var len__7211__auto___36412 = arguments.length;
var i__7212__auto___36413 = (0);
while(true){
if((i__7212__auto___36413 < len__7211__auto___36412)){
args36409.push((arguments[i__7212__auto___36413]));

var G__36414 = (i__7212__auto___36413 + (1));
i__7212__auto___36413 = G__36414;
continue;
} else {
}
break;
}

var G__36411 = args36409.length;
switch (G__36411) {
case 3:
return org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$3((arguments[(0)]),(arguments[(1)]),(arguments[(2)]));

break;
case 4:
return org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$4((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args36409.length)].join('')));

}
});

org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$3 = (function (target_id,grow_sources,die_sources){
return (new org.nfrac.comportex.synapses.SegUpdate(target_id,null,grow_sources,die_sources,null,null,null));
});

org.nfrac.comportex.synapses.seg_update.cljs$core$IFn$_invoke$arity$4 = (function (target_id,operation,grow_sources,die_sources){
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$reinforce,null,cljs.core.cst$kw$punish,null,cljs.core.cst$kw$learn,null], null), null),operation)){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$contains_QMARK_,new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$reinforce,null,cljs.core.cst$kw$punish,null,cljs.core.cst$kw$learn,null], null), null),cljs.core.cst$sym$operation)], 0)))].join('')));
}

return (new org.nfrac.comportex.synapses.SegUpdate(target_id,operation,grow_sources,die_sources,null,null,null));
});

org.nfrac.comportex.synapses.seg_update.cljs$lang$maxFixedArity = 4;
/**
 * Returns lists of synapse source ids as `[up promote down demote
 * cull]` according to whether they should be increased or decreased
 * and whether they are crossing the connected permanence threshold.
 */
org.nfrac.comportex.synapses.segment_alterations = (function org$nfrac$comportex$synapses$segment_alterations(syns,adjustable_QMARK_,reinforce_QMARK_,pcon,pinc,pdec,cull_zeros_QMARK_){
var pcon__$1 = pcon;
var pcon_PLUS_pdec = (pcon__$1 + pdec);
var pcon_pinc = (pcon__$1 - pinc);
var syns__$1 = cljs.core.seq(syns);
var up = cljs.core.List.EMPTY;
var promote = cljs.core.List.EMPTY;
var down = cljs.core.List.EMPTY;
var demote = cljs.core.List.EMPTY;
var cull = cljs.core.List.EMPTY;
while(true){
if(syns__$1){
var vec__36417 = cljs.core.first(syns__$1);
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36417,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36417,(1),null);
var p__$1 = p;
if(cljs.core.not((adjustable_QMARK_.cljs$core$IFn$_invoke$arity$1 ? adjustable_QMARK_.cljs$core$IFn$_invoke$arity$1(id) : adjustable_QMARK_.call(null,id)))){
var G__36418 = cljs.core.next(syns__$1);
var G__36419 = up;
var G__36420 = promote;
var G__36421 = down;
var G__36422 = demote;
var G__36423 = cull;
syns__$1 = G__36418;
up = G__36419;
promote = G__36420;
down = G__36421;
demote = G__36422;
cull = G__36423;
continue;
} else {
if(cljs.core.truth_((reinforce_QMARK_.cljs$core$IFn$_invoke$arity$1 ? reinforce_QMARK_.cljs$core$IFn$_invoke$arity$1(id) : reinforce_QMARK_.call(null,id)))){
var G__36424 = cljs.core.next(syns__$1);
var G__36425 = (((p__$1 < 1.0))?cljs.core.conj.cljs$core$IFn$_invoke$arity$2(up,id):up);
var G__36426 = ((((p__$1 < pcon__$1)) && ((p__$1 >= pcon_pinc)))?cljs.core.conj.cljs$core$IFn$_invoke$arity$2(promote,id):promote);
var G__36427 = down;
var G__36428 = demote;
var G__36429 = cull;
syns__$1 = G__36424;
up = G__36425;
promote = G__36426;
down = G__36427;
demote = G__36428;
cull = G__36429;
continue;
} else {
var G__36430 = cljs.core.next(syns__$1);
var G__36431 = up;
var G__36432 = promote;
var G__36433 = (((p__$1 > 0.0))?cljs.core.conj.cljs$core$IFn$_invoke$arity$2(down,id):down);
var G__36434 = ((((p__$1 >= pcon__$1)) && ((p__$1 < pcon_PLUS_pdec)))?cljs.core.conj.cljs$core$IFn$_invoke$arity$2(demote,id):demote);
var G__36435 = (cljs.core.truth_((function (){var and__6141__auto__ = (p__$1 <= 0.0);
if(and__6141__auto__){
return cull_zeros_QMARK_;
} else {
return and__6141__auto__;
}
})())?cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cull,id):cull);
syns__$1 = G__36430;
up = G__36431;
promote = G__36432;
down = G__36433;
demote = G__36434;
cull = G__36435;
continue;
}
}
} else {
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [up,promote,down,demote,cull], null);
}
break;
}
});
org.nfrac.comportex.synapses.never = (function org$nfrac$comportex$synapses$never(_){
return false;
});
org.nfrac.comportex.synapses.always = (function org$nfrac$comportex$synapses$always(_){
return true;
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.nfrac.comportex.protocols.PSynapseGraph}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.nfrac.comportex.synapses.SynapseGraph = (function (syns_by_target,targets_by_source,pcon,cull_zeros_QMARK_,__meta,__extmap,__hash){
this.syns_by_target = syns_by_target;
this.targets_by_source = targets_by_source;
this.pcon = pcon;
this.cull_zeros_QMARK_ = cull_zeros_QMARK_;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36441,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36443 = (((k36441 instanceof cljs.core.Keyword))?k36441.fqn:null);
switch (G__36443) {
case "syns-by-target":
return self__.syns_by_target;

break;
case "targets-by-source":
return self__.targets_by_source;

break;
case "pcon":
return self__.pcon;

break;
case "cull-zeros?":
return self__.cull_zeros_QMARK_;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36441,else__6770__auto__);

}
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.synapses.SynapseGraph{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$syns_DASH_by_DASH_target,self__.syns_by_target],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$targets_DASH_by_DASH_source,self__.targets_by_source],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$pcon,self__.pcon],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$cull_DASH_zeros_QMARK_,self__.cull_zeros_QMARK_],null))], null),self__.__extmap));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36440){
var self__ = this;
var G__36440__$1 = this;
return (new cljs.core.RecordIter((0),G__36440__$1,4,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$syns_DASH_by_DASH_target,cljs.core.cst$kw$targets_DASH_by_DASH_source,cljs.core.cst$kw$pcon,cljs.core.cst$kw$cull_DASH_zeros_QMARK_], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.synapses.SynapseGraph(self__.syns_by_target,self__.targets_by_source,self__.pcon,self__.cull_zeros_QMARK_,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (4 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$targets_DASH_by_DASH_source,null,cljs.core.cst$kw$syns_DASH_by_DASH_target,null,cljs.core.cst$kw$pcon,null,cljs.core.cst$kw$cull_DASH_zeros_QMARK_,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.synapses.SynapseGraph(self__.syns_by_target,self__.targets_by_source,self__.pcon,self__.cull_zeros_QMARK_,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36440){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36444 = cljs.core.keyword_identical_QMARK_;
var expr__36445 = k__6775__auto__;
if(cljs.core.truth_((pred__36444.cljs$core$IFn$_invoke$arity$2 ? pred__36444.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$syns_DASH_by_DASH_target,expr__36445) : pred__36444.call(null,cljs.core.cst$kw$syns_DASH_by_DASH_target,expr__36445)))){
return (new org.nfrac.comportex.synapses.SynapseGraph(G__36440,self__.targets_by_source,self__.pcon,self__.cull_zeros_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36444.cljs$core$IFn$_invoke$arity$2 ? pred__36444.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$targets_DASH_by_DASH_source,expr__36445) : pred__36444.call(null,cljs.core.cst$kw$targets_DASH_by_DASH_source,expr__36445)))){
return (new org.nfrac.comportex.synapses.SynapseGraph(self__.syns_by_target,G__36440,self__.pcon,self__.cull_zeros_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36444.cljs$core$IFn$_invoke$arity$2 ? pred__36444.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$pcon,expr__36445) : pred__36444.call(null,cljs.core.cst$kw$pcon,expr__36445)))){
return (new org.nfrac.comportex.synapses.SynapseGraph(self__.syns_by_target,self__.targets_by_source,G__36440,self__.cull_zeros_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36444.cljs$core$IFn$_invoke$arity$2 ? pred__36444.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$cull_DASH_zeros_QMARK_,expr__36445) : pred__36444.call(null,cljs.core.cst$kw$cull_DASH_zeros_QMARK_,expr__36445)))){
return (new org.nfrac.comportex.synapses.SynapseGraph(self__.syns_by_target,self__.targets_by_source,self__.pcon,G__36440,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.synapses.SynapseGraph(self__.syns_by_target,self__.targets_by_source,self__.pcon,self__.cull_zeros_QMARK_,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36440),null));
}
}
}
}
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$syns_DASH_by_DASH_target,self__.syns_by_target],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$targets_DASH_by_DASH_source,self__.targets_by_source],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$pcon,self__.pcon],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$cull_DASH_zeros_QMARK_,self__.cull_zeros_QMARK_],null))], null),self__.__extmap));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36440){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.synapses.SynapseGraph(self__.syns_by_target,self__.targets_by_source,self__.pcon,self__.cull_zeros_QMARK_,G__36440,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$ = true;

org.nfrac.comportex.synapses.SynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$in_synapses$arity$2 = (function (this$,target_id){
var self__ = this;
var this$__$1 = this;
return cljs.core.get.cljs$core$IFn$_invoke$arity$2(self__.syns_by_target,target_id);
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$sources_connected_to$arity$2 = (function (this$,target_id){
var self__ = this;
var this$__$1 = this;
return cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (this$__$1){
return (function (p__36447){
var vec__36448 = p__36447;
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36448,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36448,(1),null);
if((p >= self__.pcon)){
return k;
} else {
return null;
}
});})(this$__$1))
,cljs.core.get.cljs$core$IFn$_invoke$arity$2(self__.syns_by_target,target_id));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$targets_connected_from$arity$2 = (function (this$,source_id){
var self__ = this;
var this$__$1 = this;
return cljs.core.get.cljs$core$IFn$_invoke$arity$2(self__.targets_by_source,source_id);
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$excitations$arity$3 = (function (this$,active_sources,stimulus_threshold){
var self__ = this;
var this$__$1 = this;
return cljs.core.persistent_BANG_(cljs.core.reduce_kv(((function (this$__$1){
return (function (m,id,exc){
if((exc >= stimulus_threshold)){
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(m,id,exc);
} else {
return m;
}
});})(this$__$1))
,cljs.core.transient$(cljs.core.PersistentArrayMap.EMPTY),cljs.core.persistent_BANG_(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (this$__$1){
return (function (m,source_i){
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (this$__$1){
return (function (m__$1,id){
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(m__$1,id,(cljs.core.get.cljs$core$IFn$_invoke$arity$3(m__$1,id,(0)) + (1)));
});})(this$__$1))
,m,org.nfrac.comportex.protocols.targets_connected_from(this$__$1,source_i));
});})(this$__$1))
,cljs.core.transient$(cljs.core.PersistentArrayMap.EMPTY),active_sources))));
});

org.nfrac.comportex.synapses.SynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$bulk_learn$arity$6 = (function (this$,seg_updates,active_sources,pinc,pdec,pinit){
var self__ = this;
var this$__$1 = this;
var seg_updates__$1 = cljs.core.seq(seg_updates);
var syns_by_target__$1 = cljs.core.transient$(self__.syns_by_target);
var targets_by_source__$1 = cljs.core.transient$(self__.targets_by_source);
while(true){
var temp__4655__auto__ = cljs.core.first(seg_updates__$1);
if(cljs.core.truth_(temp__4655__auto__)){
var seg_up = temp__4655__auto__;
var map__36449 = seg_up;
var map__36449__$1 = ((((!((map__36449 == null)))?((((map__36449.cljs$lang$protocol_mask$partition0$ & (64))) || (map__36449.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__36449):map__36449);
var target_id = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__36449__$1,cljs.core.cst$kw$target_DASH_id);
var operation = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__36449__$1,cljs.core.cst$kw$operation);
var grow_sources = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__36449__$1,cljs.core.cst$kw$grow_DASH_sources);
var die_sources = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__36449__$1,cljs.core.cst$kw$die_DASH_sources);
var syns_STAR_ = org.nfrac.comportex.util.getx(syns_by_target__$1,target_id);
var syns = ((cljs.core.seq(die_sources))?cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc,syns_STAR_,die_sources):syns_STAR_);
var vec__36450 = (function (){var G__36452 = (((operation instanceof cljs.core.Keyword))?operation.fqn:null);
switch (G__36452) {
case "learn":
return org.nfrac.comportex.synapses.segment_alterations(syns,org.nfrac.comportex.synapses.always,active_sources,self__.pcon,pinc,pdec,self__.cull_zeros_QMARK_);

break;
case "punish":
return org.nfrac.comportex.synapses.segment_alterations(syns,active_sources,org.nfrac.comportex.synapses.never,self__.pcon,pinc,pdec,self__.cull_zeros_QMARK_);

break;
case "reinforce":
return org.nfrac.comportex.synapses.segment_alterations(syns,active_sources,org.nfrac.comportex.synapses.always,self__.pcon,pinc,pdec,self__.cull_zeros_QMARK_);

break;
default:
return new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.List.EMPTY,cljs.core.List.EMPTY,cljs.core.List.EMPTY,cljs.core.List.EMPTY,cljs.core.List.EMPTY], null);

}
})();
var up = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36450,(0),null);
var promote = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36450,(1),null);
var down = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36450,(2),null);
var demote = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36450,(3),null);
var cull = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36450,(4),null);
var new_syns = cljs.core.persistent_BANG_(cljs.core.conj_BANG_.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.util.update_each_BANG_(org.nfrac.comportex.util.update_each_BANG_(((cljs.core.seq(cull))?cljs.core.apply.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc_BANG_,cljs.core.transient$(syns),cull):cljs.core.transient$(syns)),up,((function (seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,seg_up,temp__4655__auto__,this$__$1){
return (function (p1__36436_SHARP_){
var x__6491__auto__ = (p1__36436_SHARP_ + pinc);
var y__6492__auto__ = 1.0;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
});})(seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,seg_up,temp__4655__auto__,this$__$1))
),down,((function (seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,seg_up,temp__4655__auto__,this$__$1){
return (function (p1__36437_SHARP_){
var x__6484__auto__ = (p1__36437_SHARP_ - pdec);
var y__6485__auto__ = 0.0;
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
});})(seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,seg_up,temp__4655__auto__,this$__$1))
),cljs.core.zipmap(grow_sources,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(pinit))));
var connect_ids = (((pinit >= self__.pcon))?cljs.core.concat.cljs$core$IFn$_invoke$arity$2(promote,grow_sources):promote);
var disconnect_ids = cljs.core.concat.cljs$core$IFn$_invoke$arity$2(demote,die_sources);
var G__36455 = cljs.core.next(seg_updates__$1);
var G__36456 = cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(syns_by_target__$1,target_id,new_syns);
var G__36457 = org.nfrac.comportex.util.update_each_BANG_(org.nfrac.comportex.util.update_each_BANG_(targets_by_source__$1,connect_ids,((function (seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,new_syns,connect_ids,disconnect_ids,seg_up,temp__4655__auto__,this$__$1){
return (function (p1__36438_SHARP_){
return cljs.core.conj.cljs$core$IFn$_invoke$arity$2(p1__36438_SHARP_,target_id);
});})(seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,new_syns,connect_ids,disconnect_ids,seg_up,temp__4655__auto__,this$__$1))
),disconnect_ids,((function (seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,new_syns,connect_ids,disconnect_ids,seg_up,temp__4655__auto__,this$__$1){
return (function (p1__36439_SHARP_){
return cljs.core.disj.cljs$core$IFn$_invoke$arity$2(p1__36439_SHARP_,target_id);
});})(seg_updates__$1,syns_by_target__$1,targets_by_source__$1,map__36449,map__36449__$1,target_id,operation,grow_sources,die_sources,syns_STAR_,syns,vec__36450,up,promote,down,demote,cull,new_syns,connect_ids,disconnect_ids,seg_up,temp__4655__auto__,this$__$1))
);
seg_updates__$1 = G__36455;
syns_by_target__$1 = G__36456;
targets_by_source__$1 = G__36457;
continue;
} else {
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(this$__$1,cljs.core.cst$kw$syns_DASH_by_DASH_target,cljs.core.persistent_BANG_(syns_by_target__$1),cljs.core.array_seq([cljs.core.cst$kw$targets_DASH_by_DASH_source,cljs.core.persistent_BANG_(targets_by_source__$1)], 0));
}
break;
}
});

org.nfrac.comportex.synapses.SynapseGraph.getBasis = (function (){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$syns_DASH_by_DASH_target,cljs.core.cst$sym$targets_DASH_by_DASH_source,cljs.core.cst$sym$pcon,cljs.core.cst$sym$cull_DASH_zeros_QMARK_], null);
});

org.nfrac.comportex.synapses.SynapseGraph.cljs$lang$type = true;

org.nfrac.comportex.synapses.SynapseGraph.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.synapses/SynapseGraph");
});

org.nfrac.comportex.synapses.SynapseGraph.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.synapses/SynapseGraph");
});

org.nfrac.comportex.synapses.__GT_SynapseGraph = (function org$nfrac$comportex$synapses$__GT_SynapseGraph(syns_by_target,targets_by_source,pcon,cull_zeros_QMARK_){
return (new org.nfrac.comportex.synapses.SynapseGraph(syns_by_target,targets_by_source,pcon,cull_zeros_QMARK_,null,null,null));
});

org.nfrac.comportex.synapses.map__GT_SynapseGraph = (function org$nfrac$comportex$synapses$map__GT_SynapseGraph(G__36442){
return (new org.nfrac.comportex.synapses.SynapseGraph(cljs.core.cst$kw$syns_DASH_by_DASH_target.cljs$core$IFn$_invoke$arity$1(G__36442),cljs.core.cst$kw$targets_DASH_by_DASH_source.cljs$core$IFn$_invoke$arity$1(G__36442),cljs.core.cst$kw$pcon.cljs$core$IFn$_invoke$arity$1(G__36442),cljs.core.cst$kw$cull_DASH_zeros_QMARK_.cljs$core$IFn$_invoke$arity$1(G__36442),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36442,cljs.core.cst$kw$syns_DASH_by_DASH_target,cljs.core.array_seq([cljs.core.cst$kw$targets_DASH_by_DASH_source,cljs.core.cst$kw$pcon,cljs.core.cst$kw$cull_DASH_zeros_QMARK_], 0)),null));
});

org.nfrac.comportex.synapses.empty_synapse_graph = (function org$nfrac$comportex$synapses$empty_synapse_graph(n_targets,n_sources,pcon,cull_zeros_QMARK_){
return org.nfrac.comportex.synapses.map__GT_SynapseGraph(new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$syns_DASH_by_DASH_target,cljs.core.vec(cljs.core.repeat.cljs$core$IFn$_invoke$arity$2(n_targets,cljs.core.PersistentArrayMap.EMPTY)),cljs.core.cst$kw$targets_DASH_by_DASH_source,cljs.core.vec(cljs.core.repeat.cljs$core$IFn$_invoke$arity$2(n_sources,cljs.core.PersistentHashSet.EMPTY)),cljs.core.cst$kw$pcon,pcon,cljs.core.cst$kw$cull_DASH_zeros_QMARK_,cull_zeros_QMARK_], null));
});
org.nfrac.comportex.synapses.synapse_graph = (function org$nfrac$comportex$synapses$synapse_graph(syns_by_target,n_sources,pcon,cull_zeros_QMARK_){
var targets_by_source = cljs.core.persistent_BANG_(cljs.core.reduce_kv((function (v,target_id,syns){
var connect_ids = cljs.core.keep.cljs$core$IFn$_invoke$arity$2((function (p__36461){
var vec__36462 = p__36461;
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36462,(0),null);
var p = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36462,(1),null);
if((p >= pcon)){
return i;
} else {
return null;
}
}),syns);
return org.nfrac.comportex.util.update_each_BANG_(v,connect_ids,((function (connect_ids){
return (function (p1__36458_SHARP_){
return cljs.core.conj.cljs$core$IFn$_invoke$arity$2(p1__36458_SHARP_,target_id);
});})(connect_ids))
);
}),cljs.core.transient$(cljs.core.vec(cljs.core.repeat.cljs$core$IFn$_invoke$arity$2(n_sources,cljs.core.PersistentHashSet.EMPTY))),syns_by_target));
return org.nfrac.comportex.synapses.map__GT_SynapseGraph(new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$syns_DASH_by_DASH_target,syns_by_target,cljs.core.cst$kw$targets_DASH_by_DASH_source,targets_by_source,cljs.core.cst$kw$pcon,pcon,cljs.core.cst$kw$cull_DASH_zeros_QMARK_,cull_zeros_QMARK_], null));
});
org.nfrac.comportex.synapses.seg_uidx = (function org$nfrac$comportex$synapses$seg_uidx(depth,max_segs,p__36463){
var vec__36465 = p__36463;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36465,(0),null);
var ci = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36465,(1),null);
var si = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36465,(2),null);
return ((((col * depth) * max_segs) + (ci * max_segs)) + si);
});
org.nfrac.comportex.synapses.seg_path = (function org$nfrac$comportex$synapses$seg_path(depth,max_segs,uidx){
var col = cljs.core.quot(uidx,(depth * max_segs));
var col_rem = cljs.core.rem(uidx,(depth * max_segs));
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,cljs.core.quot(col_rem,max_segs),cljs.core.rem(col_rem,max_segs)], null);
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.nfrac.comportex.protocols.PSynapseGraph}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {org.nfrac.comportex.protocols.PSegments}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.nfrac.comportex.synapses.CellSegmentsSynapseGraph = (function (int_sg,n_cols,depth,max_segs,__meta,__extmap,__hash){
this.int_sg = int_sg;
this.n_cols = n_cols;
this.depth = depth;
this.max_segs = max_segs;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36468,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36470 = (((k36468 instanceof cljs.core.Keyword))?k36468.fqn:null);
switch (G__36470) {
case "int-sg":
return self__.int_sg;

break;
case "n-cols":
return self__.n_cols;

break;
case "depth":
return self__.depth;

break;
case "max-segs":
return self__.max_segs;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36468,else__6770__auto__);

}
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.synapses.CellSegmentsSynapseGraph{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$int_DASH_sg,self__.int_sg],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$n_DASH_cols,self__.n_cols],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$depth,self__.depth],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$max_DASH_segs,self__.max_segs],null))], null),self__.__extmap));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36467){
var self__ = this;
var G__36467__$1 = this;
return (new cljs.core.RecordIter((0),G__36467__$1,4,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$int_DASH_sg,cljs.core.cst$kw$n_DASH_cols,cljs.core.cst$kw$depth,cljs.core.cst$kw$max_DASH_segs], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(self__.int_sg,self__.n_cols,self__.depth,self__.max_segs,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (4 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSegments$ = true;

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSegments$cell_segments$arity$2 = (function (this$,cell_id){
var self__ = this;
var this$__$1 = this;
var cell_id__$1 = cljs.core.vec(cell_id);
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (cell_id__$1,this$__$1){
return (function (p1__36466_SHARP_){
return org.nfrac.comportex.protocols.in_synapses(this$__$1,cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cell_id__$1,p1__36466_SHARP_));
});})(cell_id__$1,this$__$1))
,cljs.core.range.cljs$core$IFn$_invoke$arity$1(self__.max_segs));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$max_DASH_segs,null,cljs.core.cst$kw$n_DASH_cols,null,cljs.core.cst$kw$depth,null,cljs.core.cst$kw$int_DASH_sg,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(self__.int_sg,self__.n_cols,self__.depth,self__.max_segs,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36467){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36471 = cljs.core.keyword_identical_QMARK_;
var expr__36472 = k__6775__auto__;
if(cljs.core.truth_((pred__36471.cljs$core$IFn$_invoke$arity$2 ? pred__36471.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$int_DASH_sg,expr__36472) : pred__36471.call(null,cljs.core.cst$kw$int_DASH_sg,expr__36472)))){
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(G__36467,self__.n_cols,self__.depth,self__.max_segs,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36471.cljs$core$IFn$_invoke$arity$2 ? pred__36471.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$n_DASH_cols,expr__36472) : pred__36471.call(null,cljs.core.cst$kw$n_DASH_cols,expr__36472)))){
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(self__.int_sg,G__36467,self__.depth,self__.max_segs,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36471.cljs$core$IFn$_invoke$arity$2 ? pred__36471.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$depth,expr__36472) : pred__36471.call(null,cljs.core.cst$kw$depth,expr__36472)))){
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(self__.int_sg,self__.n_cols,G__36467,self__.max_segs,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36471.cljs$core$IFn$_invoke$arity$2 ? pred__36471.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$max_DASH_segs,expr__36472) : pred__36471.call(null,cljs.core.cst$kw$max_DASH_segs,expr__36472)))){
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(self__.int_sg,self__.n_cols,self__.depth,G__36467,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(self__.int_sg,self__.n_cols,self__.depth,self__.max_segs,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36467),null));
}
}
}
}
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$int_DASH_sg,self__.int_sg],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$n_DASH_cols,self__.n_cols],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$depth,self__.depth],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$max_DASH_segs,self__.max_segs],null))], null),self__.__extmap));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36467){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(self__.int_sg,self__.n_cols,self__.depth,self__.max_segs,G__36467,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$ = true;

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$in_synapses$arity$2 = (function (_,target_id){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.in_synapses(self__.int_sg,org.nfrac.comportex.synapses.seg_uidx(self__.depth,self__.max_segs,target_id));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$sources_connected_to$arity$2 = (function (_,target_id){
var self__ = this;
var ___$1 = this;
if(cljs.core.truth_(target_id)){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.cst$sym$target_DASH_id], 0)))].join('')));
}

return org.nfrac.comportex.protocols.sources_connected_to(self__.int_sg,org.nfrac.comportex.synapses.seg_uidx(self__.depth,self__.max_segs,target_id));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$targets_connected_from$arity$2 = (function (_,source_id){
var self__ = this;
var ___$1 = this;
return cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.partial.cljs$core$IFn$_invoke$arity$3(org.nfrac.comportex.synapses.seg_path,self__.depth,self__.max_segs),org.nfrac.comportex.protocols.targets_connected_from(self__.int_sg,source_id));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$excitations$arity$3 = (function (_,active_sources,stimulus_threshold){
var self__ = this;
var ___$1 = this;
var exc_m = org.nfrac.comportex.protocols.excitations(self__.int_sg,active_sources,stimulus_threshold);
return cljs.core.zipmap(cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (exc_m,___$1){
return (function (i){
return org.nfrac.comportex.synapses.seg_path(self__.depth,self__.max_segs,i);
});})(exc_m,___$1))
,cljs.core.keys(exc_m)),cljs.core.vals(exc_m));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.prototype.org$nfrac$comportex$protocols$PSynapseGraph$bulk_learn$arity$6 = (function (this$,seg_updates,active_sources,pinc,pdec,pinit){
var self__ = this;
var this$__$1 = this;
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$variadic(this$__$1,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$int_DASH_sg], null),org.nfrac.comportex.protocols.bulk_learn,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (this$__$1){
return (function (seg_up){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(seg_up,cljs.core.cst$kw$target_DASH_id,org.nfrac.comportex.synapses.seg_uidx(self__.depth,self__.max_segs,cljs.core.cst$kw$target_DASH_id.cljs$core$IFn$_invoke$arity$1(seg_up)));
});})(this$__$1))
,seg_updates),active_sources,pinc,cljs.core.array_seq([pdec,pinit], 0));
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.getBasis = (function (){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$int_DASH_sg,cljs.core.cst$sym$n_DASH_cols,cljs.core.cst$sym$depth,cljs.core.cst$sym$max_DASH_segs], null);
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.cljs$lang$type = true;

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.synapses/CellSegmentsSynapseGraph");
});

org.nfrac.comportex.synapses.CellSegmentsSynapseGraph.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.synapses/CellSegmentsSynapseGraph");
});

org.nfrac.comportex.synapses.__GT_CellSegmentsSynapseGraph = (function org$nfrac$comportex$synapses$__GT_CellSegmentsSynapseGraph(int_sg,n_cols,depth,max_segs){
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(int_sg,n_cols,depth,max_segs,null,null,null));
});

org.nfrac.comportex.synapses.map__GT_CellSegmentsSynapseGraph = (function org$nfrac$comportex$synapses$map__GT_CellSegmentsSynapseGraph(G__36469){
return (new org.nfrac.comportex.synapses.CellSegmentsSynapseGraph(cljs.core.cst$kw$int_DASH_sg.cljs$core$IFn$_invoke$arity$1(G__36469),cljs.core.cst$kw$n_DASH_cols.cljs$core$IFn$_invoke$arity$1(G__36469),cljs.core.cst$kw$depth.cljs$core$IFn$_invoke$arity$1(G__36469),cljs.core.cst$kw$max_DASH_segs.cljs$core$IFn$_invoke$arity$1(G__36469),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36469,cljs.core.cst$kw$int_DASH_sg,cljs.core.array_seq([cljs.core.cst$kw$n_DASH_cols,cljs.core.cst$kw$depth,cljs.core.cst$kw$max_DASH_segs], 0)),null));
});

/**
 * A synapse graph where the targets refer to distal dendrite
 *   segments on cells, which themselves are arranged in columns.
 *   Accordingly `target-id` is passed and returned not as an integer
 *   but as a 3-tuple `[col ci si]`, column id, cell id, segment id.
 *   Sources often refer to cells but are passed and returned as
 *   **integers**, so any conversion to/from cell ids should happen
 *   externally.
 */
org.nfrac.comportex.synapses.cell_segs_synapse_graph = (function org$nfrac$comportex$synapses$cell_segs_synapse_graph(n_cols,depth,max_segs,n_sources,pcon,cull_zeros_QMARK_){
var n_targets = ((n_cols * depth) * max_segs);
var int_sg = org.nfrac.comportex.synapses.empty_synapse_graph(n_targets,n_sources,pcon,cull_zeros_QMARK_);
return org.nfrac.comportex.synapses.map__GT_CellSegmentsSynapseGraph(new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$int_DASH_sg,int_sg,cljs.core.cst$kw$depth,depth,cljs.core.cst$kw$max_DASH_segs,max_segs], null));
});
/**
 * A synapse graph where the targets refer to proximal dendrite
 *   segments on columns.  Accordingly `target-id` is passed and returned
 *   not as an integer but as a 3-tuple `[col 0 si]`, column id, (cell = 0),
 *   segment id.  Sources often refer to cells but are passed and
 *   returned as **integers**, so any conversion to/from cell ids should
 *   happen externally.  Initial synapses are given for each segment.
 */
org.nfrac.comportex.synapses.col_segs_synapse_graph = (function org$nfrac$comportex$synapses$col_segs_synapse_graph(syns_by_col,n_cols,max_segs,n_sources,pcon,cull_zeros_QMARK_){
var n_targets = (n_cols * max_segs);
var int_syns_by_target = cljs.core.persistent_BANG_(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (n_targets){
return (function (v,p__36477){
var vec__36478 = p__36477;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36478,(0),null);
var syns = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36478,(1),null);
var path = new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0),(0)], null);
var i = org.nfrac.comportex.synapses.seg_uidx((1),max_segs,path);
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(v,i,syns);
});})(n_targets))
,cljs.core.transient$(cljs.core.vec(cljs.core.repeat.cljs$core$IFn$_invoke$arity$2(n_targets,cljs.core.PersistentArrayMap.EMPTY))),cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,syns_by_col)));
var int_sg = org.nfrac.comportex.synapses.synapse_graph(int_syns_by_target,n_sources,pcon,cull_zeros_QMARK_);
return org.nfrac.comportex.synapses.map__GT_CellSegmentsSynapseGraph(new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$int_DASH_sg,int_sg,cljs.core.cst$kw$depth,(1),cljs.core.cst$kw$max_DASH_segs,max_segs], null));
});
