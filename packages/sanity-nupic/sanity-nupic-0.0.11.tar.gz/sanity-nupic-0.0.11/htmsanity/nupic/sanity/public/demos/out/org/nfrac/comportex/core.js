// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.core');
goog.require('cljs.core');
goog.require('clojure.set');
goog.require('org.nfrac.comportex.cells');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.topology');
goog.require('org.nfrac.comportex.util.algo_graph');
goog.require('org.nfrac.comportex.util');
/**
 * A sequence of keywords looking up layers in the region. The first
 *   is the input layer, the last is the (feed-forward) output layer.
 */
org.nfrac.comportex.core.layers = (function org$nfrac$comportex$core$layers(rgn){
return cljs.core.concat.cljs$core$IFn$_invoke$arity$2((cljs.core.truth_(cljs.core.cst$kw$layer_DASH_4.cljs$core$IFn$_invoke$arity$1(rgn))?new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$layer_DASH_4], null):null),(cljs.core.truth_(cljs.core.cst$kw$layer_DASH_3.cljs$core$IFn$_invoke$arity$1(rgn))?new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$layer_DASH_3], null):null));
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {org.nfrac.comportex.protocols.PParameterised}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.nfrac.comportex.protocols.PFeedForward}
 * @implements {org.nfrac.comportex.protocols.PTemporal}
 * @implements {cljs.core.ICounted}
 * @implements {org.nfrac.comportex.protocols.PRegion}
 * @implements {org.nfrac.comportex.protocols.PFeedForwardMotor}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {org.nfrac.comportex.protocols.PFeedBack}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PInterruptable}
 * @implements {org.nfrac.comportex.protocols.PTopological}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
 * @implements {org.nfrac.comportex.protocols.PRestartable}
*/
org.nfrac.comportex.core.SensoryRegion = (function (layer_3,__meta,__extmap,__hash){
this.layer_3 = layer_3;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36900,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36902 = (((k36900 instanceof cljs.core.Keyword))?k36900.fqn:null);
switch (G__36902) {
case "layer-3":
return self__.layer_3;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36900,else__6770__auto__);

}
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.topology(self__.layer_3);
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PRestartable$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PRestartable$restart$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var G__36903 = org.nfrac.comportex.protocols.params(this$__$1);
return (org.nfrac.comportex.core.sensory_region.cljs$core$IFn$_invoke$arity$1 ? org.nfrac.comportex.core.sensory_region.cljs$core$IFn$_invoke$arity$1(G__36903) : org.nfrac.comportex.core.sensory_region.call(null,G__36903));
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.core.SensoryRegion{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layer_DASH_3,self__.layer_3],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36899){
var self__ = this;
var G__36899__$1 = this;
return (new cljs.core.RecordIter((0),G__36899__$1,1,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$layer_DASH_3], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PInterruptable$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PInterruptable$break$arity$2 = (function (this$,mode){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.protocols.break$(self__.layer_3,mode));
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.core.SensoryRegion(self__.layer_3,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$ff_motor_topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.topology.empty_topology;
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$motor_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return cljs.core.sequence.cljs$core$IFn$_invoke$arity$1(null);
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (1 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PParameterised$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PParameterised$params$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.params(self__.layer_3);
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$ff_topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.ff_topology(self__.layer_3);
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.bits_value(self__.layer_3);
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$stable_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.stable_bits_value(self__.layer_3);
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$source_of_bit$arity$2 = (function (_,i){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.source_of_bit(self__.layer_3,i);
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PTemporal$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PTemporal$timestep$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.timestep(self__.layer_3);
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$layer_DASH_3,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.core.SensoryRegion(self__.layer_3,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedBack$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PFeedBack$wc_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.wc_bits_value(self__.layer_3);
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36899){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36904 = cljs.core.keyword_identical_QMARK_;
var expr__36905 = k__6775__auto__;
if(cljs.core.truth_((pred__36904.cljs$core$IFn$_invoke$arity$2 ? pred__36904.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$layer_DASH_3,expr__36905) : pred__36904.call(null,cljs.core.cst$kw$layer_DASH_3,expr__36905)))){
return (new org.nfrac.comportex.core.SensoryRegion(G__36899,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.core.SensoryRegion(self__.layer_3,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36899),null));
}
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layer_DASH_3,self__.layer_3],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36899){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.core.SensoryRegion(self__.layer_3,G__36899,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PRegion$ = true;

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PRegion$region_activate$arity$3 = (function (this$,ff_bits,stable_ff_bits){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.protocols.layer_activate(self__.layer_3,ff_bits,stable_ff_bits));
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PRegion$region_learn$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
if(cljs.core.truth_(cljs.core.cst$kw$freeze_QMARK_.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.params(this$__$1)))){
return this$__$1;
} else {
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.protocols.layer_learn(self__.layer_3));
}
});

org.nfrac.comportex.core.SensoryRegion.prototype.org$nfrac$comportex$protocols$PRegion$region_depolarise$arity$4 = (function (this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.protocols.layer_depolarise(self__.layer_3,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits));
});

org.nfrac.comportex.core.SensoryRegion.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.core.SensoryRegion.getBasis = (function (){
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$layer_DASH_3], null);
});

org.nfrac.comportex.core.SensoryRegion.cljs$lang$type = true;

org.nfrac.comportex.core.SensoryRegion.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.core/SensoryRegion");
});

org.nfrac.comportex.core.SensoryRegion.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.core/SensoryRegion");
});

org.nfrac.comportex.core.__GT_SensoryRegion = (function org$nfrac$comportex$core$__GT_SensoryRegion(layer_3){
return (new org.nfrac.comportex.core.SensoryRegion(layer_3,null,null,null));
});

org.nfrac.comportex.core.map__GT_SensoryRegion = (function org$nfrac$comportex$core$map__GT_SensoryRegion(G__36901){
return (new org.nfrac.comportex.core.SensoryRegion(cljs.core.cst$kw$layer_DASH_3.cljs$core$IFn$_invoke$arity$1(G__36901),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(G__36901,cljs.core.cst$kw$layer_DASH_3),null));
});

/**
 * Constructs a cortical region with one layer.
 * 
 *   `spec` is the parameter specification map. See documentation on
 *   `cells/parameter-defaults` for possible keys. Any keys given here
 *   will override those default values.
 */
org.nfrac.comportex.core.sensory_region = (function org$nfrac$comportex$core$sensory_region(spec){
var unk_36908 = clojure.set.difference.cljs$core$IFn$_invoke$arity$2(cljs.core.set(cljs.core.keys(spec)),cljs.core.set(cljs.core.keys(org.nfrac.comportex.cells.parameter_defaults)));
if(cljs.core.seq(unk_36908)){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Warning: unknown keys in spec:",unk_36908], 0));
} else {
}

return org.nfrac.comportex.core.map__GT_SensoryRegion(new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.cells.layer_of_cells(spec)], null));
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {org.nfrac.comportex.protocols.PParameterised}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.nfrac.comportex.protocols.PFeedForward}
 * @implements {org.nfrac.comportex.protocols.PTemporal}
 * @implements {cljs.core.ICounted}
 * @implements {org.nfrac.comportex.protocols.PRegion}
 * @implements {org.nfrac.comportex.protocols.PFeedForwardMotor}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {org.nfrac.comportex.protocols.PFeedBack}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PInterruptable}
 * @implements {org.nfrac.comportex.protocols.PTopological}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
 * @implements {org.nfrac.comportex.protocols.PRestartable}
*/
org.nfrac.comportex.core.SensoriMotorRegion = (function (layer_4,layer_3,__meta,__extmap,__hash){
this.layer_4 = layer_4;
this.layer_3 = layer_3;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36910,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36912 = (((k36910 instanceof cljs.core.Keyword))?k36910.fqn:null);
switch (G__36912) {
case "layer-4":
return self__.layer_4;

break;
case "layer-3":
return self__.layer_3;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36910,else__6770__auto__);

}
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.topology(self__.layer_3);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PRestartable$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PRestartable$restart$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var G__36913 = org.nfrac.comportex.protocols.params(this$__$1);
return (org.nfrac.comportex.core.sensorimotor_region.cljs$core$IFn$_invoke$arity$1 ? org.nfrac.comportex.core.sensorimotor_region.cljs$core$IFn$_invoke$arity$1(G__36913) : org.nfrac.comportex.core.sensorimotor_region.call(null,G__36913));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.core.SensoriMotorRegion{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layer_DASH_4,self__.layer_4],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layer_DASH_3,self__.layer_3],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36909){
var self__ = this;
var G__36909__$1 = this;
return (new cljs.core.RecordIter((0),G__36909__$1,2,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$layer_DASH_4,cljs.core.cst$kw$layer_DASH_3], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PInterruptable$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PInterruptable$break$arity$2 = (function (this$,mode){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(this$__$1,cljs.core.cst$kw$layer_DASH_4,org.nfrac.comportex.protocols.break$(self__.layer_4,mode),cljs.core.array_seq([cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.protocols.break$(self__.layer_3,mode)], 0));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.core.SensoriMotorRegion(self__.layer_4,self__.layer_3,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$ff_motor_topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.topology.empty_topology;
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$motor_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return cljs.core.sequence.cljs$core$IFn$_invoke$arity$1(null);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (2 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PParameterised$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PParameterised$params$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.params(self__.layer_4);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$ff_topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.ff_topology(self__.layer_3);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.bits_value(self__.layer_3);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$stable_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.stable_bits_value(self__.layer_3);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedForward$source_of_bit$arity$2 = (function (_,i){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.source_of_bit(self__.layer_3,i);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PTemporal$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PTemporal$timestep$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.timestep(self__.layer_4);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$layer_DASH_4,null,cljs.core.cst$kw$layer_DASH_3,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.core.SensoriMotorRegion(self__.layer_4,self__.layer_3,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedBack$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PFeedBack$wc_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.wc_bits_value(self__.layer_3);
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36909){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36914 = cljs.core.keyword_identical_QMARK_;
var expr__36915 = k__6775__auto__;
if(cljs.core.truth_((pred__36914.cljs$core$IFn$_invoke$arity$2 ? pred__36914.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$layer_DASH_4,expr__36915) : pred__36914.call(null,cljs.core.cst$kw$layer_DASH_4,expr__36915)))){
return (new org.nfrac.comportex.core.SensoriMotorRegion(G__36909,self__.layer_3,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36914.cljs$core$IFn$_invoke$arity$2 ? pred__36914.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$layer_DASH_3,expr__36915) : pred__36914.call(null,cljs.core.cst$kw$layer_DASH_3,expr__36915)))){
return (new org.nfrac.comportex.core.SensoriMotorRegion(self__.layer_4,G__36909,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.core.SensoriMotorRegion(self__.layer_4,self__.layer_3,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36909),null));
}
}
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layer_DASH_4,self__.layer_4],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layer_DASH_3,self__.layer_3],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36909){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.core.SensoriMotorRegion(self__.layer_4,self__.layer_3,G__36909,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PRegion$ = true;

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PRegion$region_activate$arity$3 = (function (this$,ff_bits,stable_ff_bits){
var self__ = this;
var this$__$1 = this;
var l4 = org.nfrac.comportex.protocols.layer_activate(self__.layer_4,ff_bits,stable_ff_bits);
var l3 = org.nfrac.comportex.protocols.layer_activate(self__.layer_3,org.nfrac.comportex.protocols.bits_value(l4),org.nfrac.comportex.protocols.stable_bits_value(l4));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(this$__$1,cljs.core.cst$kw$layer_DASH_4,l4,cljs.core.array_seq([cljs.core.cst$kw$layer_DASH_3,l3], 0));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PRegion$region_learn$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
if(cljs.core.truth_(cljs.core.cst$kw$freeze_QMARK_.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.protocols.params(this$__$1)))){
return this$__$1;
} else {
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(this$__$1,cljs.core.cst$kw$layer_DASH_4,org.nfrac.comportex.protocols.layer_learn(self__.layer_4),cljs.core.array_seq([cljs.core.cst$kw$layer_DASH_3,org.nfrac.comportex.protocols.layer_learn(self__.layer_3)], 0));
}
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.org$nfrac$comportex$protocols$PRegion$region_depolarise$arity$4 = (function (this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits){
var self__ = this;
var this$__$1 = this;
var l4 = org.nfrac.comportex.protocols.layer_depolarise(self__.layer_4,distal_ff_bits,cljs.core.PersistentHashSet.EMPTY,cljs.core.PersistentHashSet.EMPTY);
var l3 = org.nfrac.comportex.protocols.layer_depolarise(self__.layer_3,cljs.core.PersistentHashSet.EMPTY,apical_fb_bits,apical_fb_wc_bits);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(this$__$1,cljs.core.cst$kw$layer_DASH_4,l4,cljs.core.array_seq([cljs.core.cst$kw$layer_DASH_3,l3], 0));
});

org.nfrac.comportex.core.SensoriMotorRegion.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.core.SensoriMotorRegion.getBasis = (function (){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$layer_DASH_4,cljs.core.cst$sym$layer_DASH_3], null);
});

org.nfrac.comportex.core.SensoriMotorRegion.cljs$lang$type = true;

org.nfrac.comportex.core.SensoriMotorRegion.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.core/SensoriMotorRegion");
});

org.nfrac.comportex.core.SensoriMotorRegion.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.core/SensoriMotorRegion");
});

org.nfrac.comportex.core.__GT_SensoriMotorRegion = (function org$nfrac$comportex$core$__GT_SensoriMotorRegion(layer_4,layer_3){
return (new org.nfrac.comportex.core.SensoriMotorRegion(layer_4,layer_3,null,null,null));
});

org.nfrac.comportex.core.map__GT_SensoriMotorRegion = (function org$nfrac$comportex$core$map__GT_SensoriMotorRegion(G__36911){
return (new org.nfrac.comportex.core.SensoriMotorRegion(cljs.core.cst$kw$layer_DASH_4.cljs$core$IFn$_invoke$arity$1(G__36911),cljs.core.cst$kw$layer_DASH_3.cljs$core$IFn$_invoke$arity$1(G__36911),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36911,cljs.core.cst$kw$layer_DASH_4,cljs.core.array_seq([cljs.core.cst$kw$layer_DASH_3], 0)),null));
});

/**
 * Constructs a cortical region with two layers. `spec` can contain
 *   nested maps under :layer-3 and :layer-4 that are merged in for
 *   specific layers.
 * 
 *   This sets `:lateral-synapses? false` in Layer 4, and true in Layer
 *   3.
 */
org.nfrac.comportex.core.sensorimotor_region = (function org$nfrac$comportex$core$sensorimotor_region(spec){
var unk_36918 = clojure.set.difference.cljs$core$IFn$_invoke$arity$variadic(cljs.core.set(cljs.core.keys(spec)),cljs.core.set(cljs.core.keys(org.nfrac.comportex.cells.parameter_defaults)),cljs.core.array_seq([new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$layer_DASH_4,null,cljs.core.cst$kw$layer_DASH_3,null], null), null)], 0));
if(cljs.core.seq(unk_36918)){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Warning: unknown keys in spec:",unk_36918], 0));
} else {
}

var l4_spec = cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(org.nfrac.comportex.util.deep_merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(spec,cljs.core.cst$kw$lateral_DASH_synapses_QMARK_,false),cljs.core.cst$kw$layer_DASH_4.cljs$core$IFn$_invoke$arity$2(spec,cljs.core.PersistentArrayMap.EMPTY)], 0)),cljs.core.cst$kw$layer_DASH_3,cljs.core.array_seq([cljs.core.cst$kw$layer_DASH_4], 0));
var l4 = org.nfrac.comportex.cells.layer_of_cells(l4_spec);
var l3_spec = cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(org.nfrac.comportex.util.deep_merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(spec,cljs.core.cst$kw$input_DASH_dimensions,org.nfrac.comportex.protocols.dimensions(org.nfrac.comportex.protocols.ff_topology(l4)),cljs.core.array_seq([cljs.core.cst$kw$distal_DASH_motor_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0)], null),cljs.core.cst$kw$lateral_DASH_synapses_QMARK_,true], 0)),cljs.core.cst$kw$layer_DASH_3.cljs$core$IFn$_invoke$arity$2(spec,cljs.core.PersistentArrayMap.EMPTY)], 0)),cljs.core.cst$kw$layer_DASH_3,cljs.core.array_seq([cljs.core.cst$kw$layer_DASH_4], 0));
var l3 = org.nfrac.comportex.cells.layer_of_cells(l3_spec);
return org.nfrac.comportex.core.map__GT_SensoriMotorRegion(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$layer_DASH_3,l3,cljs.core.cst$kw$layer_DASH_4,l4], null));
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.nfrac.comportex.protocols.PFeedForward}
 * @implements {cljs.core.ICounted}
 * @implements {org.nfrac.comportex.protocols.PFeedForwardMotor}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {org.nfrac.comportex.protocols.PSense}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PTopological}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.nfrac.comportex.core.SenseNode = (function (topo,bits,sensory_QMARK_,motor_QMARK_,__meta,__extmap,__hash){
this.topo = topo;
this.bits = bits;
this.sensory_QMARK_ = sensory_QMARK_;
this.motor_QMARK_ = motor_QMARK_;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.core.SenseNode.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36920,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36922 = (((k36920 instanceof cljs.core.Keyword))?k36920.fqn:null);
switch (G__36922) {
case "topo":
return self__.topo;

break;
case "bits":
return self__.bits;

break;
case "sensory?":
return self__.sensory_QMARK_;

break;
case "motor?":
return self__.motor_QMARK_;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36920,else__6770__auto__);

}
});

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.topo;
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.core.SenseNode{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$bits,self__.bits],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$sensory_QMARK_,self__.sensory_QMARK_],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$motor_QMARK_,self__.motor_QMARK_],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36919){
var self__ = this;
var G__36919__$1 = this;
return (new cljs.core.RecordIter((0),G__36919__$1,4,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$topo,cljs.core.cst$kw$bits,cljs.core.cst$kw$sensory_QMARK_,cljs.core.cst$kw$motor_QMARK_], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.core.SenseNode(self__.topo,self__.bits,self__.sensory_QMARK_,self__.motor_QMARK_,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$ = true;

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$ff_motor_topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
if(cljs.core.truth_(self__.motor_QMARK_)){
return self__.topo;
} else {
return org.nfrac.comportex.topology.empty_topology;
}
});

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForwardMotor$motor_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
if(cljs.core.truth_(self__.motor_QMARK_)){
return self__.bits;
} else {
return cljs.core.sequence.cljs$core$IFn$_invoke$arity$1(null);
}
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (4 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PSense$ = true;

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PSense$sense_activate$arity$2 = (function (this$,bits__$1){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$bits,bits__$1);
});

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForward$ = true;

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForward$ff_topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
if(cljs.core.truth_(self__.sensory_QMARK_)){
return self__.topo;
} else {
return org.nfrac.comportex.topology.empty_topology;
}
});

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForward$bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
if(cljs.core.truth_(self__.sensory_QMARK_)){
return self__.bits;
} else {
return cljs.core.sequence.cljs$core$IFn$_invoke$arity$1(null);
}
});

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForward$stable_bits_value$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return cljs.core.sequence.cljs$core$IFn$_invoke$arity$1(null);
});

org.nfrac.comportex.core.SenseNode.prototype.org$nfrac$comportex$protocols$PFeedForward$source_of_bit$arity$2 = (function (_,i){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [i], null);
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$topo,null,cljs.core.cst$kw$sensory_QMARK_,null,cljs.core.cst$kw$bits,null,cljs.core.cst$kw$motor_QMARK_,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.core.SenseNode(self__.topo,self__.bits,self__.sensory_QMARK_,self__.motor_QMARK_,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36919){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36923 = cljs.core.keyword_identical_QMARK_;
var expr__36924 = k__6775__auto__;
if(cljs.core.truth_((pred__36923.cljs$core$IFn$_invoke$arity$2 ? pred__36923.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$topo,expr__36924) : pred__36923.call(null,cljs.core.cst$kw$topo,expr__36924)))){
return (new org.nfrac.comportex.core.SenseNode(G__36919,self__.bits,self__.sensory_QMARK_,self__.motor_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36923.cljs$core$IFn$_invoke$arity$2 ? pred__36923.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$bits,expr__36924) : pred__36923.call(null,cljs.core.cst$kw$bits,expr__36924)))){
return (new org.nfrac.comportex.core.SenseNode(self__.topo,G__36919,self__.sensory_QMARK_,self__.motor_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36923.cljs$core$IFn$_invoke$arity$2 ? pred__36923.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$sensory_QMARK_,expr__36924) : pred__36923.call(null,cljs.core.cst$kw$sensory_QMARK_,expr__36924)))){
return (new org.nfrac.comportex.core.SenseNode(self__.topo,self__.bits,G__36919,self__.motor_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36923.cljs$core$IFn$_invoke$arity$2 ? pred__36923.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$motor_QMARK_,expr__36924) : pred__36923.call(null,cljs.core.cst$kw$motor_QMARK_,expr__36924)))){
return (new org.nfrac.comportex.core.SenseNode(self__.topo,self__.bits,self__.sensory_QMARK_,G__36919,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.core.SenseNode(self__.topo,self__.bits,self__.sensory_QMARK_,self__.motor_QMARK_,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36919),null));
}
}
}
}
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$bits,self__.bits],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$sensory_QMARK_,self__.sensory_QMARK_],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$motor_QMARK_,self__.motor_QMARK_],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36919){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.core.SenseNode(self__.topo,self__.bits,self__.sensory_QMARK_,self__.motor_QMARK_,G__36919,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.SenseNode.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.core.SenseNode.getBasis = (function (){
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$topo,cljs.core.cst$sym$bits,cljs.core.cst$sym$sensory_QMARK_,cljs.core.cst$sym$motor_QMARK_], null);
});

org.nfrac.comportex.core.SenseNode.cljs$lang$type = true;

org.nfrac.comportex.core.SenseNode.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.core/SenseNode");
});

org.nfrac.comportex.core.SenseNode.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.core/SenseNode");
});

org.nfrac.comportex.core.__GT_SenseNode = (function org$nfrac$comportex$core$__GT_SenseNode(topo,bits,sensory_QMARK_,motor_QMARK_){
return (new org.nfrac.comportex.core.SenseNode(topo,bits,sensory_QMARK_,motor_QMARK_,null,null,null));
});

org.nfrac.comportex.core.map__GT_SenseNode = (function org$nfrac$comportex$core$map__GT_SenseNode(G__36921){
return (new org.nfrac.comportex.core.SenseNode(cljs.core.cst$kw$topo.cljs$core$IFn$_invoke$arity$1(G__36921),cljs.core.cst$kw$bits.cljs$core$IFn$_invoke$arity$1(G__36921),cljs.core.cst$kw$sensory_QMARK_.cljs$core$IFn$_invoke$arity$1(G__36921),cljs.core.cst$kw$motor_QMARK_.cljs$core$IFn$_invoke$arity$1(G__36921),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36921,cljs.core.cst$kw$topo,cljs.core.array_seq([cljs.core.cst$kw$bits,cljs.core.cst$kw$sensory_QMARK_,cljs.core.cst$kw$motor_QMARK_], 0)),null));
});

/**
 * Creates a sense node with given topology, matching the encoder that
 *   will generate its bits.
 */
org.nfrac.comportex.core.sense_node = (function org$nfrac$comportex$core$sense_node(topo,sensory_QMARK_,motor_QMARK_){
return org.nfrac.comportex.core.__GT_SenseNode(topo,cljs.core.List.EMPTY,sensory_QMARK_,motor_QMARK_);
});
/**
 * Returns the total bit set from a collection of sources satisfying
 * `PFeedForward` or `PFeedForwardMotor`. `flavour` should
 * be :standard, :stable or :motor.
 */
org.nfrac.comportex.core.combined_bits_value = (function org$nfrac$comportex$core$combined_bits_value(ffs,flavour){
var topo_fn = (function (){var G__36929 = (((flavour instanceof cljs.core.Keyword))?flavour.fqn:null);
switch (G__36929) {
case "standard":
return org.nfrac.comportex.protocols.ff_topology;

break;
case "stable":
return org.nfrac.comportex.protocols.ff_topology;

break;
case "wc":
return org.nfrac.comportex.protocols.ff_topology;

break;
case "motor":
return org.nfrac.comportex.protocols.ff_motor_topology;

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(flavour)].join('')));

}
})();
var bits_fn = (function (){var G__36930 = (((flavour instanceof cljs.core.Keyword))?flavour.fqn:null);
switch (G__36930) {
case "standard":
return org.nfrac.comportex.protocols.bits_value;

break;
case "stable":
return org.nfrac.comportex.protocols.stable_bits_value;

break;
case "wc":
return org.nfrac.comportex.protocols.wc_bits_value;

break;
case "motor":
return org.nfrac.comportex.protocols.motor_bits_value;

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(flavour)].join('')));

}
})();
var widths = cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.comp.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.protocols.size,topo_fn),ffs);
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentHashSet.EMPTY,org.nfrac.comportex.util.align_indices.cljs$core$IFn$_invoke$arity$2(widths,cljs.core.map.cljs$core$IFn$_invoke$arity$2(bits_fn,ffs)));
});
/**
 * Taking the index of an input bit as received by the given region,
 *   return its source element as [k id] where k is the key of the source
 *   region or sense, and id is the index adjusted to refer to the output
 *   of that source.
 * 
 *   If i is an index into the feed-forward field, type is :ff-deps, if i
 *   is an index into the feed-back field, type is :fb-deps.
 */
org.nfrac.comportex.core.source_of_incoming_bit = (function org$nfrac$comportex$core$source_of_incoming_bit(var_args){
var args36933 = [];
var len__7211__auto___36936 = arguments.length;
var i__7212__auto___36937 = (0);
while(true){
if((i__7212__auto___36937 < len__7211__auto___36936)){
args36933.push((arguments[i__7212__auto___36937]));

var G__36938 = (i__7212__auto___36937 + (1));
i__7212__auto___36937 = G__36938;
continue;
} else {
}
break;
}

var G__36935 = args36933.length;
switch (G__36935) {
case 4:
return org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]));

break;
case 5:
return org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$5((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]),(arguments[(4)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args36933.length)].join('')));

}
});

org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4 = (function (htm,rgn_id,i,type){
return org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$5(htm,rgn_id,i,type,org.nfrac.comportex.protocols.ff_topology);
});

org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$5 = (function (htm,rgn_id,i,type,topology_fn){
var senses = cljs.core.cst$kw$senses.cljs$core$IFn$_invoke$arity$1(htm);
var regions = cljs.core.cst$kw$regions.cljs$core$IFn$_invoke$arity$1(htm);
var node_ids = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [type,rgn_id], null));
var node_ids__$1 = node_ids;
var offset = (0);
while(true){
var temp__4657__auto__ = cljs.core.first(node_ids__$1);
if(cljs.core.truth_(temp__4657__auto__)){
var node_id = temp__4657__auto__;
var node = (function (){var or__6153__auto__ = (senses.cljs$core$IFn$_invoke$arity$1 ? senses.cljs$core$IFn$_invoke$arity$1(node_id) : senses.call(null,node_id));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return (regions.cljs$core$IFn$_invoke$arity$1 ? regions.cljs$core$IFn$_invoke$arity$1(node_id) : regions.call(null,node_id));
}
})();
var width = cljs.core.long$(org.nfrac.comportex.protocols.size((topology_fn.cljs$core$IFn$_invoke$arity$1 ? topology_fn.cljs$core$IFn$_invoke$arity$1(node) : topology_fn.call(null,node))));
if((i < (offset + width))){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [node_id,(i - offset)], null);
} else {
var G__36940 = cljs.core.next(node_ids__$1);
var G__36941 = (offset + width);
node_ids__$1 = G__36940;
offset = G__36941;
continue;
}
} else {
return null;
}
break;
}
});

org.nfrac.comportex.core.source_of_incoming_bit.cljs$lang$maxFixedArity = 5;
/**
 * Returns [src-id src-lyr-id j] where src-id may be a region key or
 * sense key, src-lyr-id is nil for senses, and j is the index into
 * the output of the source.
 */
org.nfrac.comportex.core.source_of_distal_bit = (function org$nfrac$comportex$core$source_of_distal_bit(htm,rgn_id,lyr_id,i){
var rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id], null));
var lyr = cljs.core.get.cljs$core$IFn$_invoke$arity$2(rgn,lyr_id);
var spec = org.nfrac.comportex.protocols.params(lyr);
var vec__36945 = org.nfrac.comportex.cells.id__GT_source(spec,i);
var src_type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36945,(0),null);
var adj_i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36945,(1),null);
var G__36946 = (((src_type instanceof cljs.core.Keyword))?src_type.fqn:null);
switch (G__36946) {
case "this":
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [rgn_id,lyr_id,i], null);

break;
case "ff":
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(lyr_id,cljs.core.first(org.nfrac.comportex.core.layers(rgn)))){
var vec__36947 = org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$5(htm,rgn_id,adj_i,cljs.core.cst$kw$ff_DASH_deps,org.nfrac.comportex.protocols.ff_motor_topology);
var src_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36947,(0),null);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36947,(1),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_id], null));
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [src_id,(cljs.core.truth_(src_rgn)?cljs.core.last(org.nfrac.comportex.core.layers(src_rgn)):null),j], null);
} else {
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [rgn_id,cljs.core.first(org.nfrac.comportex.core.layers(rgn)),i], null);
}

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(src_type)].join('')));

}
});
/**
 * Returns [src-id src-lyr-id j] where src-id is a region key, and j
 *   is the index into the output of the region.
 */
org.nfrac.comportex.core.source_of_apical_bit = (function org$nfrac$comportex$core$source_of_apical_bit(htm,rgn_id,lyr_id,i){
var rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id], null));
var lyr = cljs.core.get.cljs$core$IFn$_invoke$arity$2(rgn,lyr_id);
var spec = org.nfrac.comportex.protocols.params(lyr);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(lyr_id,cljs.core.last(org.nfrac.comportex.core.layers(rgn)))){
var vec__36950 = org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4(htm,rgn_id,i,cljs.core.cst$kw$fb_DASH_deps);
var src_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36950,(0),null);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36950,(1),null);
var src_rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,src_id], null));
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [src_id,cljs.core.last(org.nfrac.comportex.core.layers(src_rgn)),j], null);
} else {
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [rgn_id,cljs.core.last(org.nfrac.comportex.core.layers(rgn)),i], null);
}
});
org.nfrac.comportex.core.topo_union = (function org$nfrac$comportex$core$topo_union(topos){
return cljs.core.apply.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.topology.combined_dimensions,cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.protocols.dimensions,topos));
});
org.nfrac.comportex.core.fb_dim_from_spec = (function org$nfrac$comportex$core$fb_dim_from_spec(spec){
var spec__$1 = org.nfrac.comportex.util.deep_merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([org.nfrac.comportex.cells.parameter_defaults,spec], 0));
return org.nfrac.comportex.topology.make_topology(cljs.core.conj.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$column_DASH_dimensions.cljs$core$IFn$_invoke$arity$1(spec__$1),cljs.core.cst$kw$depth.cljs$core$IFn$_invoke$arity$1(spec__$1)));
});
org.nfrac.comportex.core.pmap = cljs.core.map;

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.nfrac.comportex.protocols.PTemporal}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {org.nfrac.comportex.protocols.PHTM}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PInterruptable}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
 * @implements {org.nfrac.comportex.protocols.PRestartable}
*/
org.nfrac.comportex.core.RegionNetwork = (function (ff_deps,fb_deps,strata,sensors,senses,regions,__meta,__extmap,__hash){
this.ff_deps = ff_deps;
this.fb_deps = fb_deps;
this.strata = strata;
this.sensors = sensors;
this.senses = senses;
this.regions = regions;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k36954,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__36956 = (((k36954 instanceof cljs.core.Keyword))?k36954.fqn:null);
switch (G__36956) {
case "ff-deps":
return self__.ff_deps;

break;
case "fb-deps":
return self__.fb_deps;

break;
case "strata":
return self__.strata;

break;
case "sensors":
return self__.sensors;

break;
case "senses":
return self__.senses;

break;
case "regions":
return self__.regions;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k36954,else__6770__auto__);

}
});

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PRestartable$ = true;

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PRestartable$restart$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$regions,cljs.core.zipmap(cljs.core.keys(self__.regions),(function (){var G__36957 = org.nfrac.comportex.protocols.restart;
var G__36958 = cljs.core.vals(self__.regions);
return (org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2 ? org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2(G__36957,G__36958) : org.nfrac.comportex.core.pmap.call(null,G__36957,G__36958));
})()));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.nfrac.comportex.core.RegionNetwork{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ff_DASH_deps,self__.ff_deps],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$fb_DASH_deps,self__.fb_deps],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$strata,self__.strata],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$sensors,self__.sensors],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$senses,self__.senses],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$regions,self__.regions],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IIterable$ = true;

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__36953){
var self__ = this;
var G__36953__$1 = this;
return (new cljs.core.RecordIter((0),G__36953__$1,6,new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ff_DASH_deps,cljs.core.cst$kw$fb_DASH_deps,cljs.core.cst$kw$strata,cljs.core.cst$kw$sensors,cljs.core.cst$kw$senses,cljs.core.cst$kw$regions], null),cljs.core._iterator(self__.__extmap)));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PInterruptable$ = true;

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PInterruptable$break$arity$2 = (function (this$,mode){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$regions,cljs.core.zipmap(cljs.core.keys(self__.regions),cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (this$__$1){
return (function (p1__36952_SHARP_){
return org.nfrac.comportex.protocols.break$(p1__36952_SHARP_,mode);
});})(this$__$1))
,cljs.core.vals(self__.regions))));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,self__.strata,self__.sensors,self__.senses,self__.regions,self__.__meta,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (6 + cljs.core.count(self__.__extmap));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PHTM$ = true;

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PHTM$htm_sense$arity$3 = (function (this$,inval,mode){
var self__ = this;
var this$__$1 = this;
var sm = cljs.core.reduce_kv(((function (this$__$1){
return (function (m,k,sense_node){
if(cljs.core.truth_((function (){var G__36959 = mode;
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$sensory,G__36959)){
return cljs.core.cst$kw$sensory_QMARK_.cljs$core$IFn$_invoke$arity$1(sense_node);
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$motor,G__36959)){
return cljs.core.cst$kw$motor_QMARK_.cljs$core$IFn$_invoke$arity$1(sense_node);
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(null,G__36959)){
return true;
} else {
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(mode)].join('')));

}
}
}
})())){
var vec__36960 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(self__.sensors,k);
var selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36960,(0),null);
var encoder = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36960,(1),null);
var in_bits = org.nfrac.comportex.protocols.encode(encoder,org.nfrac.comportex.protocols.extract(selector,inval));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(m,k,org.nfrac.comportex.protocols.sense_activate(sense_node,in_bits));
} else {
return m;
}
});})(this$__$1))
,self__.senses,self__.senses);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(this$__$1,cljs.core.cst$kw$senses,sm,cljs.core.array_seq([cljs.core.cst$kw$input_DASH_value,inval], 0));
});

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PHTM$htm_activate$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var rm = cljs.core.select_keys(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (this$__$1){
return (function (m,stratum){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(m,cljs.core.zipmap(stratum,(function (){var G__36961 = ((function (this$__$1){
return (function (id){
var region = (self__.regions.cljs$core$IFn$_invoke$arity$1 ? self__.regions.cljs$core$IFn$_invoke$arity$1(id) : self__.regions.call(null,id));
var ff_ids = (self__.ff_deps.cljs$core$IFn$_invoke$arity$1 ? self__.ff_deps.cljs$core$IFn$_invoke$arity$1(id) : self__.ff_deps.call(null,id));
var ffs = cljs.core.map.cljs$core$IFn$_invoke$arity$2(m,ff_ids);
return org.nfrac.comportex.protocols.region_activate(region,org.nfrac.comportex.core.combined_bits_value(ffs,cljs.core.cst$kw$standard),org.nfrac.comportex.core.combined_bits_value(ffs,cljs.core.cst$kw$stable));
});})(this$__$1))
;
var G__36962 = stratum;
return (org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2 ? org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2(G__36961,G__36962) : org.nfrac.comportex.core.pmap.call(null,G__36961,G__36962));
})()));
});})(this$__$1))
,self__.senses,cljs.core.rest(self__.strata)),cljs.core.keys(self__.regions));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$regions,rm);
});

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PHTM$htm_learn$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var rm = cljs.core.zipmap(cljs.core.keys(self__.regions),(function (){var G__36963 = org.nfrac.comportex.protocols.region_learn;
var G__36964 = cljs.core.vals(self__.regions);
return (org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2 ? org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2(G__36963,G__36964) : org.nfrac.comportex.core.pmap.call(null,G__36963,G__36964));
})());
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$regions,rm);
});

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PHTM$htm_depolarise$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var rm = cljs.core.zipmap(cljs.core.keys(self__.regions),(function (){var G__36967 = ((function (this$__$1){
return (function (p__36969){
var vec__36970 = p__36969;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36970,(0),null);
var region = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36970,(1),null);
var ff_ids = (self__.ff_deps.cljs$core$IFn$_invoke$arity$1 ? self__.ff_deps.cljs$core$IFn$_invoke$arity$1(id) : self__.ff_deps.call(null,id));
var fb_ids = (self__.fb_deps.cljs$core$IFn$_invoke$arity$1 ? self__.fb_deps.cljs$core$IFn$_invoke$arity$1(id) : self__.fb_deps.call(null,id));
var ffs = cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (ff_ids,fb_ids,vec__36970,id,region,this$__$1){
return (function (p1__36951_SHARP_){
var or__6153__auto__ = (self__.senses.cljs$core$IFn$_invoke$arity$1 ? self__.senses.cljs$core$IFn$_invoke$arity$1(p1__36951_SHARP_) : self__.senses.call(null,p1__36951_SHARP_));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return (self__.regions.cljs$core$IFn$_invoke$arity$1 ? self__.regions.cljs$core$IFn$_invoke$arity$1(p1__36951_SHARP_) : self__.regions.call(null,p1__36951_SHARP_));
}
});})(ff_ids,fb_ids,vec__36970,id,region,this$__$1))
,ff_ids);
var fbs = cljs.core.map.cljs$core$IFn$_invoke$arity$2(self__.regions,fb_ids);
return org.nfrac.comportex.protocols.region_depolarise(region,org.nfrac.comportex.core.combined_bits_value(ffs,cljs.core.cst$kw$motor),org.nfrac.comportex.core.combined_bits_value(fbs,cljs.core.cst$kw$standard),org.nfrac.comportex.core.combined_bits_value(fbs,cljs.core.cst$kw$wc));
});})(this$__$1))
;
var G__36968 = self__.regions;
return (org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2 ? org.nfrac.comportex.core.pmap.cljs$core$IFn$_invoke$arity$2(G__36967,G__36968) : org.nfrac.comportex.core.pmap.call(null,G__36967,G__36968));
})());
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$regions,rm);
});

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PTemporal$ = true;

org.nfrac.comportex.core.RegionNetwork.prototype.org$nfrac$comportex$protocols$PTemporal$timestep$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.timestep(cljs.core.first(cljs.core.vals(self__.regions)));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$senses,null,cljs.core.cst$kw$ff_DASH_deps,null,cljs.core.cst$kw$fb_DASH_deps,null,cljs.core.cst$kw$regions,null,cljs.core.cst$kw$sensors,null,cljs.core.cst$kw$strata,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,self__.strata,self__.sensors,self__.senses,self__.regions,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__36953){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__36971 = cljs.core.keyword_identical_QMARK_;
var expr__36972 = k__6775__auto__;
if(cljs.core.truth_((pred__36971.cljs$core$IFn$_invoke$arity$2 ? pred__36971.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$ff_DASH_deps,expr__36972) : pred__36971.call(null,cljs.core.cst$kw$ff_DASH_deps,expr__36972)))){
return (new org.nfrac.comportex.core.RegionNetwork(G__36953,self__.fb_deps,self__.strata,self__.sensors,self__.senses,self__.regions,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36971.cljs$core$IFn$_invoke$arity$2 ? pred__36971.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$fb_DASH_deps,expr__36972) : pred__36971.call(null,cljs.core.cst$kw$fb_DASH_deps,expr__36972)))){
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,G__36953,self__.strata,self__.sensors,self__.senses,self__.regions,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36971.cljs$core$IFn$_invoke$arity$2 ? pred__36971.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$strata,expr__36972) : pred__36971.call(null,cljs.core.cst$kw$strata,expr__36972)))){
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,G__36953,self__.sensors,self__.senses,self__.regions,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36971.cljs$core$IFn$_invoke$arity$2 ? pred__36971.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$sensors,expr__36972) : pred__36971.call(null,cljs.core.cst$kw$sensors,expr__36972)))){
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,self__.strata,G__36953,self__.senses,self__.regions,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36971.cljs$core$IFn$_invoke$arity$2 ? pred__36971.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$senses,expr__36972) : pred__36971.call(null,cljs.core.cst$kw$senses,expr__36972)))){
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,self__.strata,self__.sensors,G__36953,self__.regions,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__36971.cljs$core$IFn$_invoke$arity$2 ? pred__36971.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$regions,expr__36972) : pred__36971.call(null,cljs.core.cst$kw$regions,expr__36972)))){
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,self__.strata,self__.sensors,self__.senses,G__36953,self__.__meta,self__.__extmap,null));
} else {
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,self__.strata,self__.sensors,self__.senses,self__.regions,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__36953),null));
}
}
}
}
}
}
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ff_DASH_deps,self__.ff_deps],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$fb_DASH_deps,self__.fb_deps],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$strata,self__.strata],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$sensors,self__.sensors],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$senses,self__.senses],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$regions,self__.regions],null))], null),self__.__extmap));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__36953){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.nfrac.comportex.core.RegionNetwork(self__.ff_deps,self__.fb_deps,self__.strata,self__.sensors,self__.senses,self__.regions,G__36953,self__.__extmap,self__.__hash));
});

org.nfrac.comportex.core.RegionNetwork.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.nfrac.comportex.core.RegionNetwork.getBasis = (function (){
return new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$ff_DASH_deps,cljs.core.cst$sym$fb_DASH_deps,cljs.core.cst$sym$strata,cljs.core.cst$sym$sensors,cljs.core.cst$sym$senses,cljs.core.cst$sym$regions], null);
});

org.nfrac.comportex.core.RegionNetwork.cljs$lang$type = true;

org.nfrac.comportex.core.RegionNetwork.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.nfrac.comportex.core/RegionNetwork");
});

org.nfrac.comportex.core.RegionNetwork.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.nfrac.comportex.core/RegionNetwork");
});

org.nfrac.comportex.core.__GT_RegionNetwork = (function org$nfrac$comportex$core$__GT_RegionNetwork(ff_deps,fb_deps,strata,sensors,senses,regions){
return (new org.nfrac.comportex.core.RegionNetwork(ff_deps,fb_deps,strata,sensors,senses,regions,null,null,null));
});

org.nfrac.comportex.core.map__GT_RegionNetwork = (function org$nfrac$comportex$core$map__GT_RegionNetwork(G__36955){
return (new org.nfrac.comportex.core.RegionNetwork(cljs.core.cst$kw$ff_DASH_deps.cljs$core$IFn$_invoke$arity$1(G__36955),cljs.core.cst$kw$fb_DASH_deps.cljs$core$IFn$_invoke$arity$1(G__36955),cljs.core.cst$kw$strata.cljs$core$IFn$_invoke$arity$1(G__36955),cljs.core.cst$kw$sensors.cljs$core$IFn$_invoke$arity$1(G__36955),cljs.core.cst$kw$senses.cljs$core$IFn$_invoke$arity$1(G__36955),cljs.core.cst$kw$regions.cljs$core$IFn$_invoke$arity$1(G__36955),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__36955,cljs.core.cst$kw$ff_DASH_deps,cljs.core.array_seq([cljs.core.cst$kw$fb_DASH_deps,cljs.core.cst$kw$strata,cljs.core.cst$kw$sensors,cljs.core.cst$kw$senses,cljs.core.cst$kw$regions], 0)),null));
});

/**
 * A sequence of the keys of all regions in topologically-sorted
 *   order. If `n-levels` is provided, only the regions from that many
 *   hierarchical levels are included. So 1 gives the first tier directly
 *   receiving sensory inputs.
 */
org.nfrac.comportex.core.region_keys = (function org$nfrac$comportex$core$region_keys(var_args){
var args36975 = [];
var len__7211__auto___36978 = arguments.length;
var i__7212__auto___36979 = (0);
while(true){
if((i__7212__auto___36979 < len__7211__auto___36978)){
args36975.push((arguments[i__7212__auto___36979]));

var G__36980 = (i__7212__auto___36979 + (1));
i__7212__auto___36979 = G__36980;
continue;
} else {
}
break;
}

var G__36977 = args36975.length;
switch (G__36977) {
case 1:
return org.nfrac.comportex.core.region_keys.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.nfrac.comportex.core.region_keys.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args36975.length)].join('')));

}
});

org.nfrac.comportex.core.region_keys.cljs$core$IFn$_invoke$arity$1 = (function (htm){
return org.nfrac.comportex.core.region_keys.cljs$core$IFn$_invoke$arity$2(htm,(cljs.core.count(cljs.core.cst$kw$strata.cljs$core$IFn$_invoke$arity$1(htm)) - (1)));
});

org.nfrac.comportex.core.region_keys.cljs$core$IFn$_invoke$arity$2 = (function (htm,n_levels){
return cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.concat,cljs.core.take.cljs$core$IFn$_invoke$arity$2(n_levels,cljs.core.rest(cljs.core.cst$kw$strata.cljs$core$IFn$_invoke$arity$1(htm))));
});

org.nfrac.comportex.core.region_keys.cljs$lang$maxFixedArity = 2;
/**
 * A sequence of the keys of all sense nodes.
 */
org.nfrac.comportex.core.sense_keys = (function org$nfrac$comportex$core$sense_keys(htm){
return cljs.core.first(cljs.core.cst$kw$strata.cljs$core$IFn$_invoke$arity$1(htm));
});
org.nfrac.comportex.core.region_seq = (function org$nfrac$comportex$core$region_seq(htm){
return cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$regions.cljs$core$IFn$_invoke$arity$1(htm),org.nfrac.comportex.core.region_keys.cljs$core$IFn$_invoke$arity$1(htm));
});
org.nfrac.comportex.core.in_vals_not_keys = (function org$nfrac$comportex$core$in_vals_not_keys(deps){
var have_deps = cljs.core.set(cljs.core.keys(deps));
var are_deps = cljs.core.set(cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.concat,cljs.core.vals(deps)));
return clojure.set.difference.cljs$core$IFn$_invoke$arity$2(are_deps,have_deps);
});
/**
 * Builds a network of regions and senses from the given dependency
 *   map. The keywords used in the dependency map are used to look up
 *   region-building functions, parameter specifications, and sensors in
 *   the remaining argments.
 * 
 *   Sensors are defined to be the form `[selector encoder]`, satisfying
 *   protocols PSelector and PEncoder respectively. Sensors in the
 *   `main-sensors` map can make activating (proximal) connections while
 *   those in the `motor-sensors` map can make depolarising (distal)
 *   connections. The same sensor may also be included in both maps.
 * 
 *   For each node, the combined dimensions of its feed-forward sources
 *   is calculated and used to set the `:input-dimensions` parameter in
 *   its `spec`. Also, the combined dimensions of feed-forward motor
 *   inputs are used to set the `:distal-motor-dimensions` parameter, and
 *   the combined dimensions of its feed-back superior regions is used to
 *   set the `:distal-topdown-dimensions` parameter. The updated spec is
 *   passed to a function (typically `sensory-region`) to build a
 *   region. The build function is found by calling `region-builders`
 *   with the region id keyword.
 * 
 *   For example to build the network `inp -> v1 -> v2`:
 * 
 * `
 * (region-network
 *  {:v1 [:input]
 *   :v2 [:v1]}
 *  {:v1 sensory-region
 *   :v2 sensory-region}
 *  {:v1 spec
 *   :v2 spec}
 *  {:input sensor}
 *  nil)`
 */
org.nfrac.comportex.core.region_network = (function org$nfrac$comportex$core$region_network(ff_deps,region_builders,region_specs,main_sensors,motor_sensors){
if(cljs.core.every_QMARK_(ff_deps,cljs.core.keys(region_specs))){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$every_QMARK_,cljs.core.cst$sym$ff_DASH_deps,cljs.core.list(cljs.core.cst$sym$keys,cljs.core.cst$sym$region_DASH_specs))], 0)))].join('')));
}

if(cljs.core.every_QMARK_(org.nfrac.comportex.core.in_vals_not_keys(ff_deps),cljs.core.keys(main_sensors))){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$every_QMARK_,cljs.core.list(cljs.core.cst$sym$in_DASH_vals_DASH_not_DASH_keys,cljs.core.cst$sym$ff_DASH_deps),cljs.core.list(cljs.core.cst$sym$keys,cljs.core.cst$sym$main_DASH_sensors))], 0)))].join('')));
}

if(cljs.core.every_QMARK_(org.nfrac.comportex.core.in_vals_not_keys(ff_deps),cljs.core.keys(motor_sensors))){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$every_QMARK_,cljs.core.list(cljs.core.cst$sym$in_DASH_vals_DASH_not_DASH_keys,cljs.core.cst$sym$ff_DASH_deps),cljs.core.list(cljs.core.cst$sym$keys,cljs.core.cst$sym$motor_DASH_sensors))], 0)))].join('')));
}

if(cljs.core.every_QMARK_(region_specs,cljs.core.keys(ff_deps))){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$every_QMARK_,cljs.core.cst$sym$region_DASH_specs,cljs.core.list(cljs.core.cst$sym$keys,cljs.core.cst$sym$ff_DASH_deps))], 0)))].join('')));
}

if(cljs.core.every_QMARK_(cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([main_sensors,motor_sensors], 0)),org.nfrac.comportex.core.in_vals_not_keys(ff_deps))){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$every_QMARK_,cljs.core.list(cljs.core.cst$sym$merge,cljs.core.cst$sym$main_DASH_sensors,cljs.core.cst$sym$motor_DASH_sensors),cljs.core.list(cljs.core.cst$sym$in_DASH_vals_DASH_not_DASH_keys,cljs.core.cst$sym$ff_DASH_deps))], 0)))].join('')));
}

cljs.core.merge_with.cljs$core$IFn$_invoke$arity$variadic((function (main_sensor,motor_sensor){
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(main_sensor,motor_sensor)){
return null;
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str("Equal keys in main-sensors and motor-sensors must be same sensor."),cljs.core.str("\n"),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$_EQ_,cljs.core.cst$sym$main_DASH_sensor,cljs.core.cst$sym$motor_DASH_sensor)], 0)))].join('')));
}
}),cljs.core.array_seq([main_sensors,motor_sensors], 0));

var all_ids = cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.set(cljs.core.keys(ff_deps)),org.nfrac.comportex.core.in_vals_not_keys(ff_deps));
var ff_dag = org.nfrac.comportex.util.algo_graph.directed_graph(all_ids,ff_deps);
var strata = org.nfrac.comportex.util.algo_graph.dependency_list(ff_dag);
var fb_deps = org.nfrac.comportex.util.remap(cljs.core.seq,cljs.core.cst$kw$neighbors.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.util.algo_graph.reverse_graph(ff_dag)));
var sm = org.nfrac.comportex.util.remap(((function (all_ids,ff_dag,strata,fb_deps){
return (function (p__36990){
var map__36991 = p__36990;
var map__36991__$1 = ((((!((map__36991 == null)))?((((map__36991.cljs$lang$protocol_mask$partition0$ & (64))) || (map__36991.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__36991):map__36991);
var topo = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__36991__$1,cljs.core.cst$kw$topo);
var sensory_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__36991__$1,cljs.core.cst$kw$sensory_QMARK_);
var motor_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__36991__$1,cljs.core.cst$kw$motor_QMARK_);
return org.nfrac.comportex.core.sense_node(topo,sensory_QMARK_,motor_QMARK_);
});})(all_ids,ff_dag,strata,fb_deps))
,cljs.core.merge_with.cljs$core$IFn$_invoke$arity$variadic(cljs.core.merge,cljs.core.array_seq([org.nfrac.comportex.util.remap(((function (all_ids,ff_dag,strata,fb_deps){
return (function (p__36993){
var vec__36994 = p__36993;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36994,(0),null);
var e = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36994,(1),null);
return new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$topo,org.nfrac.comportex.protocols.topology(e),cljs.core.cst$kw$sensory_QMARK_,true], null);
});})(all_ids,ff_dag,strata,fb_deps))
,main_sensors),org.nfrac.comportex.util.remap(((function (all_ids,ff_dag,strata,fb_deps){
return (function (p__36995){
var vec__36996 = p__36995;
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36996,(0),null);
var e = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__36996,(1),null);
return new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$topo,org.nfrac.comportex.protocols.topology(e),cljs.core.cst$kw$motor_QMARK_,true], null);
});})(all_ids,ff_dag,strata,fb_deps))
,motor_sensors)], 0)));
var rm = cljs.core.select_keys(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (all_ids,ff_dag,strata,fb_deps,sm){
return (function (m,id){
var spec = (region_specs.cljs$core$IFn$_invoke$arity$1 ? region_specs.cljs$core$IFn$_invoke$arity$1(id) : region_specs.call(null,id));
var build_region = (region_builders.cljs$core$IFn$_invoke$arity$1 ? region_builders.cljs$core$IFn$_invoke$arity$1(id) : region_builders.call(null,id));
var ff_ids = (ff_deps.cljs$core$IFn$_invoke$arity$1 ? ff_deps.cljs$core$IFn$_invoke$arity$1(id) : ff_deps.call(null,id));
var ffs = cljs.core.map.cljs$core$IFn$_invoke$arity$2(m,ff_ids);
var ff_dim = org.nfrac.comportex.core.topo_union(cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.protocols.ff_topology,ffs));
var ffm_dim = org.nfrac.comportex.core.topo_union(cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.protocols.ff_motor_topology,ffs));
var fb_ids = (fb_deps.cljs$core$IFn$_invoke$arity$1 ? fb_deps.cljs$core$IFn$_invoke$arity$1(id) : fb_deps.call(null,id));
var fb_specs = cljs.core.map.cljs$core$IFn$_invoke$arity$2(region_specs,fb_ids);
var fb_dim = org.nfrac.comportex.core.topo_union(cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.core.fb_dim_from_spec,fb_specs));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(m,id,(function (){var G__36997 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(spec,cljs.core.cst$kw$input_DASH_dimensions,ff_dim,cljs.core.array_seq([cljs.core.cst$kw$distal_DASH_motor_DASH_dimensions,ffm_dim,cljs.core.cst$kw$distal_DASH_topdown_DASH_dimensions,fb_dim], 0));
return (build_region.cljs$core$IFn$_invoke$arity$1 ? build_region.cljs$core$IFn$_invoke$arity$1(G__36997) : build_region.call(null,G__36997));
})());
});})(all_ids,ff_dag,strata,fb_deps,sm))
,sm,cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.concat,cljs.core.rest(strata))),cljs.core.keys(region_specs));
return org.nfrac.comportex.core.map__GT_RegionNetwork(new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$ff_DASH_deps,ff_deps,cljs.core.cst$kw$fb_DASH_deps,fb_deps,cljs.core.cst$kw$strata,strata,cljs.core.cst$kw$sensors,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([main_sensors,motor_sensors], 0)),cljs.core.cst$kw$senses,sm,cljs.core.cst$kw$regions,rm], null));
});
/**
 * Constructs an HTM network consisting of n regions in a linear
 *   series. The regions are given keys :rgn-0, :rgn-1, etc. Senses feed
 *   only to the first region. Their sensors are given in a map with
 *   keyword keys. Sensors are defined to be the form `[selector encoder]`.
 * 
 *   This is a convenience wrapper around `region-network`.
 */
org.nfrac.comportex.core.regions_in_series = (function org$nfrac$comportex$core$regions_in_series(var_args){
var args36999 = [];
var len__7211__auto___37002 = arguments.length;
var i__7212__auto___37003 = (0);
while(true){
if((i__7212__auto___37003 < len__7211__auto___37002)){
args36999.push((arguments[i__7212__auto___37003]));

var G__37004 = (i__7212__auto___37003 + (1));
i__7212__auto___37003 = G__37004;
continue;
} else {
}
break;
}

var G__37001 = args36999.length;
switch (G__37001) {
case 4:
return org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$4((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]));

break;
case 5:
return org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$5((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]),(arguments[(4)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args36999.length)].join('')));

}
});

org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$4 = (function (n,build_region,specs,sensors){
return org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$5(n,build_region,specs,sensors,null);
});

org.nfrac.comportex.core.regions_in_series.cljs$core$IFn$_invoke$arity$5 = (function (n,build_region,specs,main_sensors,motor_sensors){
if(cljs.core.sequential_QMARK_(specs)){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$sequential_QMARK_,cljs.core.cst$sym$specs)], 0)))].join('')));
}

if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(n,cljs.core.count(cljs.core.take.cljs$core$IFn$_invoke$arity$2(n,specs)))){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$_EQ_,cljs.core.cst$sym$n,cljs.core.list(cljs.core.cst$sym$count,cljs.core.list(cljs.core.cst$sym$take,cljs.core.cst$sym$n,cljs.core.cst$sym$specs)))], 0)))].join('')));
}

var rgn_keys = cljs.core.map.cljs$core$IFn$_invoke$arity$2((function (p1__36998_SHARP_){
return cljs.core.keyword.cljs$core$IFn$_invoke$arity$1([cljs.core.str("rgn-"),cljs.core.str(p1__36998_SHARP_)].join(''));
}),cljs.core.range.cljs$core$IFn$_invoke$arity$1(n));
var sense_keys = cljs.core.keys(cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([main_sensors,motor_sensors], 0)));
var deps = cljs.core.zipmap(rgn_keys,cljs.core.list_STAR_.cljs$core$IFn$_invoke$arity$2(sense_keys,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,rgn_keys)));
return org.nfrac.comportex.core.region_network(deps,cljs.core.constantly(build_region),cljs.core.zipmap(rgn_keys,specs),main_sensors,motor_sensors);
});

org.nfrac.comportex.core.regions_in_series.cljs$lang$maxFixedArity = 5;
/**
 * Returns a map with the frequencies of columns in states
 *   `:active` (bursting), `:predicted`, `:active-predicted`. Note that
 *   these are distinct categories. The names are possibly misleading.
 *   Argument `layer-fn` is called on the region to obtain a layer of
 *   cells; if omitted it defaults to the output layer.
 */
org.nfrac.comportex.core.column_state_freqs = (function org$nfrac$comportex$core$column_state_freqs(var_args){
var args37006 = [];
var len__7211__auto___37009 = arguments.length;
var i__7212__auto___37010 = (0);
while(true){
if((i__7212__auto___37010 < len__7211__auto___37009)){
args37006.push((arguments[i__7212__auto___37010]));

var G__37011 = (i__7212__auto___37010 + (1));
i__7212__auto___37010 = G__37011;
continue;
} else {
}
break;
}

var G__37008 = args37006.length;
switch (G__37008) {
case 1:
return org.nfrac.comportex.core.column_state_freqs.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.nfrac.comportex.core.column_state_freqs.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args37006.length)].join('')));

}
});

org.nfrac.comportex.core.column_state_freqs.cljs$core$IFn$_invoke$arity$1 = (function (rgn){
return org.nfrac.comportex.core.column_state_freqs.cljs$core$IFn$_invoke$arity$2(rgn,cljs.core.last(org.nfrac.comportex.core.layers(rgn)));
});

org.nfrac.comportex.core.column_state_freqs.cljs$core$IFn$_invoke$arity$2 = (function (rgn,layer_fn){
var lyr = (layer_fn.cljs$core$IFn$_invoke$arity$1 ? layer_fn.cljs$core$IFn$_invoke$arity$1(rgn) : layer_fn.call(null,rgn));
var a_cols = org.nfrac.comportex.protocols.active_columns(lyr);
var ppc = org.nfrac.comportex.protocols.prior_predictive_cells(lyr);
var pp_cols = cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentHashSet.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.first,ppc));
var hit_cols = clojure.set.intersection.cljs$core$IFn$_invoke$arity$2(pp_cols,a_cols);
var col_states = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.zipmap(pp_cols,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$predicted)),cljs.core.zipmap(a_cols,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$active)),cljs.core.zipmap(hit_cols,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$active_DASH_predicted))], 0));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$active,(0),cljs.core.cst$kw$predicted,(0),cljs.core.cst$kw$active_DASH_predicted,(0)], null),cljs.core.frequencies(cljs.core.vals(col_states))], 0)),cljs.core.cst$kw$timestep,org.nfrac.comportex.protocols.timestep(rgn),cljs.core.array_seq([cljs.core.cst$kw$size,org.nfrac.comportex.protocols.size(org.nfrac.comportex.protocols.topology(rgn))], 0));
});

org.nfrac.comportex.core.column_state_freqs.cljs$lang$maxFixedArity = 2;
org.nfrac.comportex.core.segs_proximal_bit_votes = (function org$nfrac$comportex$core$segs_proximal_bit_votes(lyr,seg_paths){
var psg = cljs.core.cst$kw$proximal_DASH_sg.cljs$core$IFn$_invoke$arity$1(lyr);
return cljs.core.persistent_BANG_(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (psg){
return (function (m,seg_path){
var ids = org.nfrac.comportex.protocols.sources_connected_to(psg,seg_path);
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (ids,psg){
return (function (m__$1,id){
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(m__$1,id,(cljs.core.get.cljs$core$IFn$_invoke$arity$3(m__$1,id,(0)) + (1)));
});})(ids,psg))
,m,ids);
});})(psg))
,cljs.core.transient$(cljs.core.PersistentArrayMap.EMPTY),seg_paths));
});
/**
 * For decoding. Given a set of cells in the layer, returns a map from
 *   incoming bit index to the number of connections to that bit from the
 *   cells' columns.
 */
org.nfrac.comportex.core.cells_proximal_bit_votes = (function org$nfrac$comportex$core$cells_proximal_bit_votes(lyr,cells){
return org.nfrac.comportex.core.segs_proximal_bit_votes(lyr,cljs.core.map.cljs$core$IFn$_invoke$arity$2((function (p1__37013_SHARP_){
return cljs.core.conj.cljs$core$IFn$_invoke$arity$2(p1__37013_SHARP_,(0));
}),cells));
});
org.nfrac.comportex.core.predicted_bit_votes = (function org$nfrac$comportex$core$predicted_bit_votes(rgn){
var lyr = cljs.core.get.cljs$core$IFn$_invoke$arity$2(rgn,cljs.core.first(org.nfrac.comportex.core.layers(rgn)));
var pc = org.nfrac.comportex.protocols.predictive_cells(lyr);
return org.nfrac.comportex.core.cells_proximal_bit_votes(lyr,pc);
});
/**
 * Returns the first index that corresponds with `ff-id` within the
 *   feedforward input to `rgn-id`.
 */
org.nfrac.comportex.core.ff_base = (function org$nfrac$comportex$core$ff_base(htm,rgn_id,ff_id){
var map__37020 = htm;
var map__37020__$1 = ((((!((map__37020 == null)))?((((map__37020.cljs$lang$protocol_mask$partition0$ & (64))) || (map__37020.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__37020):map__37020);
var senses = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__37020__$1,cljs.core.cst$kw$senses);
var regions = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__37020__$1,cljs.core.cst$kw$regions);
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._PLUS_,(0),cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.protocols.size,cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.protocols.ff_topology,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (map__37020,map__37020__$1,senses,regions){
return (function (p__37022){
var vec__37023 = p__37022;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37023,(0),null);
var ff = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37023,(1),null);
return ff;
});})(map__37020,map__37020__$1,senses,regions))
,cljs.core.take_while.cljs$core$IFn$_invoke$arity$2(((function (map__37020,map__37020__$1,senses,regions){
return (function (p__37024){
var vec__37025 = p__37024;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37025,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37025,(1),null);
return cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2(id,ff_id);
});})(map__37020,map__37020__$1,senses,regions))
,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (map__37020,map__37020__$1,senses,regions){
return (function (id){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [id,(function (){var or__6153__auto__ = (senses.cljs$core$IFn$_invoke$arity$1 ? senses.cljs$core$IFn$_invoke$arity$1(id) : senses.call(null,id));
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return (regions.cljs$core$IFn$_invoke$arity$1 ? regions.cljs$core$IFn$_invoke$arity$1(id) : regions.call(null,id));
}
})()], null);
});})(map__37020,map__37020__$1,senses,regions))
,cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ff_DASH_deps,rgn_id], null))))))));
});
org.nfrac.comportex.core.predictions = (function org$nfrac$comportex$core$predictions(var_args){
var args37026 = [];
var len__7211__auto___37034 = arguments.length;
var i__7212__auto___37035 = (0);
while(true){
if((i__7212__auto___37035 < len__7211__auto___37034)){
args37026.push((arguments[i__7212__auto___37035]));

var G__37036 = (i__7212__auto___37035 + (1));
i__7212__auto___37035 = G__37036;
continue;
} else {
}
break;
}

var G__37028 = args37026.length;
switch (G__37028) {
case 3:
return org.nfrac.comportex.core.predictions.cljs$core$IFn$_invoke$arity$3((arguments[(0)]),(arguments[(1)]),(arguments[(2)]));

break;
case 4:
return org.nfrac.comportex.core.predictions.cljs$core$IFn$_invoke$arity$4((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args37026.length)].join('')));

}
});

org.nfrac.comportex.core.predictions.cljs$core$IFn$_invoke$arity$3 = (function (htm,sense_id,n_predictions){
return org.nfrac.comportex.core.predictions.cljs$core$IFn$_invoke$arity$4(htm,sense_id,n_predictions,org.nfrac.comportex.protocols.predictive_cells);
});

org.nfrac.comportex.core.predictions.cljs$core$IFn$_invoke$arity$4 = (function (htm,sense_id,n_predictions,cells_fn){
var sense_width = org.nfrac.comportex.protocols.size(org.nfrac.comportex.protocols.ff_topology(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$senses,sense_id], null))));
var pr_votes = cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (sense_width){
return (function (m,p__37030){
var vec__37031 = p__37030;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37031,(0),null);
var votes = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37031,(1),null);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(m,id,(cljs.core.get.cljs$core$IFn$_invoke$arity$3(m,id,(0)) + votes));
});})(sense_width))
,cljs.core.PersistentArrayMap.EMPTY,cljs.core.mapcat.cljs$core$IFn$_invoke$arity$variadic(((function (sense_width){
return (function (rgn_id){
var rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id], null));
var start = org.nfrac.comportex.core.ff_base(htm,rgn_id,sense_id);
var end = (start + sense_width);
var lyr = cljs.core.get.cljs$core$IFn$_invoke$arity$2(rgn,cljs.core.first(org.nfrac.comportex.core.layers(rgn)));
var cells = (cells_fn.cljs$core$IFn$_invoke$arity$1 ? cells_fn.cljs$core$IFn$_invoke$arity$1(lyr) : cells_fn.call(null,lyr));
return cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (rgn,start,end,lyr,cells,sense_width){
return (function (p__37032){
var vec__37033 = p__37032;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37033,(0),null);
var votes = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37033,(1),null);
if(((start <= id)) && ((id < end))){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(id - start),votes], null);
} else {
return null;
}
});})(rgn,start,end,lyr,cells,sense_width))
,org.nfrac.comportex.core.cells_proximal_bit_votes(lyr,cells));
});})(sense_width))
,cljs.core.array_seq([cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$fb_DASH_deps,sense_id], null))], 0)));
var vec__37029 = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$sensors,sense_id], null));
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37029,(0),null);
var encoder = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37029,(1),null);
return org.nfrac.comportex.protocols.decode(encoder,pr_votes,n_predictions);
});

org.nfrac.comportex.core.predictions.cljs$lang$maxFixedArity = 4;
org.nfrac.comportex.core.zap_fewer = (function org$nfrac$comportex$core$zap_fewer(n,xs){
if((cljs.core.count(xs) < n)){
return cljs.core.empty(xs);
} else {
return xs;
}
});
/**
 * Calculates the various sources contributing to total excitation
 *   level of each of the `cell-ids` in the given layer. Returns a map
 *   keyed by these cell ids. Each cell value is a map with keys
 * 
 *   * :total - number.
 *   * :proximal-unstable - a map keyed by source region/sense id.
 *   * :proximal-stable - a map keyed by source region/sense id.
 *   * :distal - a map keyed by source region/sense id.
 *   * :boost - number.
 *   
 */
org.nfrac.comportex.core.cell_excitation_breakdowns = (function org$nfrac$comportex$core$cell_excitation_breakdowns(htm,prior_htm,rgn_id,lyr_id,cell_ids){
var rgn = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id], null));
var lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id,lyr_id], null));
var prior_lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(prior_htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id,lyr_id], null));
var spec = cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(lyr);
var ff_stim_thresh = cljs.core.cst$kw$stimulus_DASH_threshold.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$proximal.cljs$core$IFn$_invoke$arity$1(spec));
var d_stim_thresh = cljs.core.cst$kw$stimulus_DASH_threshold.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$distal.cljs$core$IFn$_invoke$arity$1(spec));
var a_stim_thresh = cljs.core.cst$kw$stimulus_DASH_threshold.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$apical.cljs$core$IFn$_invoke$arity$1(spec));
var distal_weight = cljs.core.cst$kw$distal_DASH_vs_DASH_proximal_DASH_weight.cljs$core$IFn$_invoke$arity$1(spec);
var state = cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr);
var prior_state = cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(prior_lyr);
var distal_state = cljs.core.cst$kw$distal_DASH_state.cljs$core$IFn$_invoke$arity$1(prior_lyr);
var apical_state = cljs.core.cst$kw$apical_DASH_state.cljs$core$IFn$_invoke$arity$1(prior_lyr);
var ff_bits = cljs.core.cst$kw$in_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(state);
var ff_s_bits = cljs.core.cst$kw$in_DASH_stable_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(state);
var ff_b_bits = clojure.set.difference.cljs$core$IFn$_invoke$arity$2(ff_bits,ff_s_bits);
var distal_bits = cljs.core.cst$kw$active_DASH_bits.cljs$core$IFn$_invoke$arity$1(distal_state);
var apical_bits = cljs.core.cst$kw$active_DASH_bits.cljs$core$IFn$_invoke$arity$1(apical_state);
var is_input_layer_QMARK_ = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(lyr_id,cljs.core.first(org.nfrac.comportex.core.layers(rgn)));
var ff_bits_srcs = ((is_input_layer_QMARK_)?cljs.core.into.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$1(((function (rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_){
return (function (i){
var vec__37047 = org.nfrac.comportex.core.source_of_incoming_bit.cljs$core$IFn$_invoke$arity$4(htm,rgn_id,i,cljs.core.cst$kw$ff_DASH_bits);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37047,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37047,(1),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,k], null);
});})(rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_))
),ff_bits):cljs.core.constantly(rgn_id));
var distal_bits_srcs = cljs.core.into.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$1(((function (rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs){
return (function (i){
var vec__37048 = org.nfrac.comportex.core.source_of_distal_bit(htm,rgn_id,lyr_id,i);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37048,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37048,(1),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,k], null);
});})(rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs))
),distal_bits);
var apical_bits_srcs = cljs.core.into.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$1(((function (rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs){
return (function (i){
var vec__37049 = org.nfrac.comportex.core.source_of_apical_bit(htm,rgn_id,lyr_id,i);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37049,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37049,(1),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,k], null);
});})(rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs))
),apical_bits);
var psg = cljs.core.cst$kw$proximal_DASH_sg.cljs$core$IFn$_invoke$arity$1(prior_lyr);
var dsg = cljs.core.cst$kw$distal_DASH_sg.cljs$core$IFn$_invoke$arity$1(prior_lyr);
var asg = cljs.core.cst$kw$apical_DASH_sg.cljs$core$IFn$_invoke$arity$1(prior_lyr);
var boosts = cljs.core.cst$kw$boosts.cljs$core$IFn$_invoke$arity$1(prior_lyr);
return cljs.core.into.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentArrayMap.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$1(((function (rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs,apical_bits_srcs,psg,dsg,asg,boosts){
return (function (cell_id){
var vec__37050 = cell_id;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37050,(0),null);
var ci = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37050,(1),null);
var vec__37051 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$matching_DASH_ff_DASH_seg_DASH_paths.cljs$core$IFn$_invoke$arity$1(state),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [col,(0)], null));
var ff_seg_path = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37051,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37051,(1),null);
var ff_conn_sources = (cljs.core.truth_(ff_seg_path)?org.nfrac.comportex.protocols.sources_connected_to(psg,ff_seg_path):null);
var active_ff_b = org.nfrac.comportex.core.zap_fewer(ff_stim_thresh,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(ff_b_bits,ff_conn_sources));
var active_ff_s = org.nfrac.comportex.core.zap_fewer(ff_stim_thresh,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(ff_s_bits,ff_conn_sources));
var ff_b_by_src = cljs.core.frequencies(cljs.core.map.cljs$core$IFn$_invoke$arity$2(ff_bits_srcs,active_ff_b));
var ff_s_by_src = cljs.core.frequencies(cljs.core.map.cljs$core$IFn$_invoke$arity$2(ff_bits_srcs,active_ff_s));
var vec__37052 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$matching_DASH_seg_DASH_paths.cljs$core$IFn$_invoke$arity$1(distal_state),cell_id);
var d_seg_path = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37052,(0),null);
var ___$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37052,(1),null);
var d_conn_sources = (cljs.core.truth_(d_seg_path)?org.nfrac.comportex.protocols.sources_connected_to(dsg,d_seg_path):null);
var active_d = org.nfrac.comportex.core.zap_fewer(d_stim_thresh,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(distal_bits,d_conn_sources));
var d_by_src = org.nfrac.comportex.util.remap(((function (vec__37050,col,ci,vec__37051,ff_seg_path,_,ff_conn_sources,active_ff_b,active_ff_s,ff_b_by_src,ff_s_by_src,vec__37052,d_seg_path,___$1,d_conn_sources,active_d,rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs,apical_bits_srcs,psg,dsg,asg,boosts){
return (function (p1__37038_SHARP_){
return (p1__37038_SHARP_ * distal_weight);
});})(vec__37050,col,ci,vec__37051,ff_seg_path,_,ff_conn_sources,active_ff_b,active_ff_s,ff_b_by_src,ff_s_by_src,vec__37052,d_seg_path,___$1,d_conn_sources,active_d,rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs,apical_bits_srcs,psg,dsg,asg,boosts))
,cljs.core.frequencies(cljs.core.map.cljs$core$IFn$_invoke$arity$2(distal_bits_srcs,active_d)));
var vec__37053 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$matching_DASH_seg_DASH_paths.cljs$core$IFn$_invoke$arity$1(apical_state),cell_id);
var a_seg_path = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37053,(0),null);
var ___$2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__37053,(1),null);
var a_conn_sources = (cljs.core.truth_(a_seg_path)?org.nfrac.comportex.protocols.sources_connected_to(asg,a_seg_path):null);
var active_a = org.nfrac.comportex.core.zap_fewer(a_stim_thresh,cljs.core.filter.cljs$core$IFn$_invoke$arity$2(apical_bits,a_conn_sources));
var a_by_src = org.nfrac.comportex.util.remap(((function (vec__37050,col,ci,vec__37051,ff_seg_path,_,ff_conn_sources,active_ff_b,active_ff_s,ff_b_by_src,ff_s_by_src,vec__37052,d_seg_path,___$1,d_conn_sources,active_d,d_by_src,vec__37053,a_seg_path,___$2,a_conn_sources,active_a,rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs,apical_bits_srcs,psg,dsg,asg,boosts){
return (function (p1__37039_SHARP_){
return (p1__37039_SHARP_ * distal_weight);
});})(vec__37050,col,ci,vec__37051,ff_seg_path,_,ff_conn_sources,active_ff_b,active_ff_s,ff_b_by_src,ff_s_by_src,vec__37052,d_seg_path,___$1,d_conn_sources,active_d,d_by_src,vec__37053,a_seg_path,___$2,a_conn_sources,active_a,rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs,apical_bits_srcs,psg,dsg,asg,boosts))
,cljs.core.frequencies(cljs.core.map.cljs$core$IFn$_invoke$arity$2(apical_bits_srcs,active_a)));
var b_overlap = cljs.core.count(active_ff_b);
var s_overlap = cljs.core.count(active_ff_s);
var d_a_exc = (distal_weight * (cljs.core.count(active_d) + cljs.core.count(active_a)));
var overlap = (b_overlap + s_overlap);
var boost_amt = (overlap * (cljs.core.get.cljs$core$IFn$_invoke$arity$2(boosts,col) - 1.0));
var total = (((b_overlap + s_overlap) + boost_amt) + d_a_exc);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cell_id,new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$total,total,cljs.core.cst$kw$proximal_DASH_unstable,ff_b_by_src,cljs.core.cst$kw$proximal_DASH_stable,ff_s_by_src,cljs.core.cst$kw$boost,boost_amt,cljs.core.cst$kw$distal,cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([d_by_src,a_by_src], 0))], null)], null);
});})(rgn,lyr,prior_lyr,spec,ff_stim_thresh,d_stim_thresh,a_stim_thresh,distal_weight,state,prior_state,distal_state,apical_state,ff_bits,ff_s_bits,ff_b_bits,distal_bits,apical_bits,is_input_layer_QMARK_,ff_bits_srcs,distal_bits_srcs,apical_bits_srcs,psg,dsg,asg,boosts))
),cell_ids);
});
/**
 * Takes an excitation breakdown such as returned under one key from
 *   cell-excitation-breakdowns, and updates each numeric component with
 *   the function f. Key :total will be updated accordingly. The default
 *   is to scale the values to a total of 1.0. To aggregate breakdowns,
 *   use `(util/deep-merge-with +)`.
 */
org.nfrac.comportex.core.update_excitation_breakdown = (function org$nfrac$comportex$core$update_excitation_breakdown(var_args){
var args37055 = [];
var len__7211__auto___37058 = arguments.length;
var i__7212__auto___37059 = (0);
while(true){
if((i__7212__auto___37059 < len__7211__auto___37058)){
args37055.push((arguments[i__7212__auto___37059]));

var G__37060 = (i__7212__auto___37059 + (1));
i__7212__auto___37059 = G__37060;
continue;
} else {
}
break;
}

var G__37057 = args37055.length;
switch (G__37057) {
case 1:
return org.nfrac.comportex.core.update_excitation_breakdown.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
case 2:
return org.nfrac.comportex.core.update_excitation_breakdown.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args37055.length)].join('')));

}
});

org.nfrac.comportex.core.update_excitation_breakdown.cljs$core$IFn$_invoke$arity$1 = (function (breakdown){
var total = cljs.core.cst$kw$total.cljs$core$IFn$_invoke$arity$1(breakdown);
return org.nfrac.comportex.core.update_excitation_breakdown.cljs$core$IFn$_invoke$arity$2(breakdown,((function (total){
return (function (p1__37054_SHARP_){
return (p1__37054_SHARP_ / total);
});})(total))
);
});

org.nfrac.comportex.core.update_excitation_breakdown.cljs$core$IFn$_invoke$arity$2 = (function (breakdown,f){
return cljs.core.persistent_BANG_(cljs.core.reduce_kv((function (m,k,v){
var new_v = ((cljs.core.map_QMARK_(v))?org.nfrac.comportex.util.remap(f,v):(f.cljs$core$IFn$_invoke$arity$1 ? f.cljs$core$IFn$_invoke$arity$1(v) : f.call(null,v)));
var v_total = ((cljs.core.map_QMARK_(v))?cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core._PLUS_,cljs.core.vals(new_v)):new_v);
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$variadic(m,k,new_v,cljs.core.array_seq([cljs.core.cst$kw$total,(cljs.core.get.cljs$core$IFn$_invoke$arity$2(m,cljs.core.cst$kw$total) + v_total)], 0));
}),cljs.core.transient$(new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$total,0.0], null)),cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(breakdown,cljs.core.cst$kw$total)));
});

org.nfrac.comportex.core.update_excitation_breakdown.cljs$lang$maxFixedArity = 2;
