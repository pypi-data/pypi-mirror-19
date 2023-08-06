// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.protocols');
goog.require('cljs.core');

/**
 * A network of regions and senses, forming Hierarchical Temporal Memory.
 * @interface
 */
org.nfrac.comportex.protocols.PHTM = function(){};

/**
 * Takes an input value. Updates the HTM's senses by applying
 *  corresponding sensors to the input value. `mode` may be
 *  :sensory or :motor to update only such senses, or nil to update
 *  all. Also updates :input-value. Returns updated HTM.
 */
org.nfrac.comportex.protocols.htm_sense = (function org$nfrac$comportex$protocols$htm_sense(this$,inval,mode){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PHTM$htm_sense$arity$3 == null)))){
return this$.org$nfrac$comportex$protocols$PHTM$htm_sense$arity$3(this$,inval,mode);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.htm_sense[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,inval,mode) : m__6809__auto__.call(null,this$,inval,mode));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.htm_sense["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,inval,mode) : m__6809__auto____$1.call(null,this$,inval,mode));
} else {
throw cljs.core.missing_protocol("PHTM.htm-sense",this$);
}
}
}
});

/**
 * Propagates feed-forward input through the network to activate
 *  columns and cells. Assumes senses have already been encoded, with
 *  `htm-sense`. Increments the time step. Returns updated HTM.
 */
org.nfrac.comportex.protocols.htm_activate = (function org$nfrac$comportex$protocols$htm_activate(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PHTM$htm_activate$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PHTM$htm_activate$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.htm_activate[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.htm_activate["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PHTM.htm-activate",this$);
}
}
}
});

/**
 * Applies learning rules to synapses. Assumes `this` has been through
 *  the `htm-activate` phase already. Returns updated HTM.
 */
org.nfrac.comportex.protocols.htm_learn = (function org$nfrac$comportex$protocols$htm_learn(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PHTM$htm_learn$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PHTM$htm_learn$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.htm_learn[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.htm_learn["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PHTM.htm-learn",this$);
}
}
}
});

/**
 * Propagates lateral and feed-back activity to put cells into a
 *  depolarised (predictive) state. Assumes `this` has been through
 *  the `htm-activate` phase already. Returns updated HTM.
 */
org.nfrac.comportex.protocols.htm_depolarise = (function org$nfrac$comportex$protocols$htm_depolarise(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PHTM$htm_depolarise$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PHTM$htm_depolarise$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.htm_depolarise[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.htm_depolarise["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PHTM.htm-depolarise",this$);
}
}
}
});

/**
 * Advances a HTM by a full time step with the given input value. Just
 *   (-> htm (htm-sense inval nil) htm-activate htm-learn htm-depolarise)
 */
org.nfrac.comportex.protocols.htm_step = (function org$nfrac$comportex$protocols$htm_step(htm,inval){
return org.nfrac.comportex.protocols.htm_depolarise(org.nfrac.comportex.protocols.htm_learn(org.nfrac.comportex.protocols.htm_activate(org.nfrac.comportex.protocols.htm_sense(htm,inval,null))));
});

/**
 * Cortical regions need to extend this together with PTopological,
 * PFeedForward, PTemporal, PParameterised.
 * @interface
 */
org.nfrac.comportex.protocols.PRegion = function(){};

org.nfrac.comportex.protocols.region_activate = (function org$nfrac$comportex$protocols$region_activate(this$,ff_bits,stable_ff_bits){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PRegion$region_activate$arity$3 == null)))){
return this$.org$nfrac$comportex$protocols$PRegion$region_activate$arity$3(this$,ff_bits,stable_ff_bits);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.region_activate[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,ff_bits,stable_ff_bits) : m__6809__auto__.call(null,this$,ff_bits,stable_ff_bits));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.region_activate["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,ff_bits,stable_ff_bits) : m__6809__auto____$1.call(null,this$,ff_bits,stable_ff_bits));
} else {
throw cljs.core.missing_protocol("PRegion.region-activate",this$);
}
}
}
});

org.nfrac.comportex.protocols.region_learn = (function org$nfrac$comportex$protocols$region_learn(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PRegion$region_learn$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PRegion$region_learn$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.region_learn[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.region_learn["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PRegion.region-learn",this$);
}
}
}
});

org.nfrac.comportex.protocols.region_depolarise = (function org$nfrac$comportex$protocols$region_depolarise(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PRegion$region_depolarise$arity$4 == null)))){
return this$.org$nfrac$comportex$protocols$PRegion$region_depolarise$arity$4(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.region_depolarise[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$4(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits) : m__6809__auto__.call(null,this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.region_depolarise["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits) : m__6809__auto____$1.call(null,this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits));
} else {
throw cljs.core.missing_protocol("PRegion.region-depolarise",this$);
}
}
}
});

org.nfrac.comportex.protocols.region_step = (function org$nfrac$comportex$protocols$region_step(var_args){
var args36253 = [];
var len__7211__auto___36256 = arguments.length;
var i__7212__auto___36257 = (0);
while(true){
if((i__7212__auto___36257 < len__7211__auto___36256)){
args36253.push((arguments[i__7212__auto___36257]));

var G__36258 = (i__7212__auto___36257 + (1));
i__7212__auto___36257 = G__36258;
continue;
} else {
}
break;
}

var G__36255 = args36253.length;
switch (G__36255) {
case 2:
return org.nfrac.comportex.protocols.region_step.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
case 6:
return org.nfrac.comportex.protocols.region_step.cljs$core$IFn$_invoke$arity$6((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]),(arguments[(4)]),(arguments[(5)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args36253.length)].join('')));

}
});

org.nfrac.comportex.protocols.region_step.cljs$core$IFn$_invoke$arity$2 = (function (this$,ff_bits){
return org.nfrac.comportex.protocols.region_step.cljs$core$IFn$_invoke$arity$6(this$,ff_bits,cljs.core.PersistentHashSet.EMPTY,cljs.core.PersistentHashSet.EMPTY,cljs.core.PersistentHashSet.EMPTY,cljs.core.PersistentHashSet.EMPTY);
});

org.nfrac.comportex.protocols.region_step.cljs$core$IFn$_invoke$arity$6 = (function (this$,ff_bits,stable_ff_bits,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits){
return org.nfrac.comportex.protocols.region_depolarise(org.nfrac.comportex.protocols.region_learn(org.nfrac.comportex.protocols.region_activate(this$,ff_bits,stable_ff_bits)),distal_ff_bits,apical_fb_bits,apical_fb_wc_bits);
});

org.nfrac.comportex.protocols.region_step.cljs$lang$maxFixedArity = 6;

/**
 * A feed-forward input source with a bit set representation. Could be
 * sensory input or a region (where cells are bits).
 * @interface
 */
org.nfrac.comportex.protocols.PFeedForward = function(){};

org.nfrac.comportex.protocols.ff_topology = (function org$nfrac$comportex$protocols$ff_topology(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PFeedForward$ff_topology$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PFeedForward$ff_topology$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.ff_topology[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.ff_topology["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PFeedForward.ff-topology",this$);
}
}
}
});

/**
 * The set of indices of all active bits/cells.
 */
org.nfrac.comportex.protocols.bits_value = (function org$nfrac$comportex$protocols$bits_value(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PFeedForward$bits_value$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PFeedForward$bits_value$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.bits_value[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.bits_value["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PFeedForward.bits-value",this$);
}
}
}
});

/**
 * The set of indices of active cells where those cells were
 *  predicted (so, excluding cells from bursting columns).
 */
org.nfrac.comportex.protocols.stable_bits_value = (function org$nfrac$comportex$protocols$stable_bits_value(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PFeedForward$stable_bits_value$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PFeedForward$stable_bits_value$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.stable_bits_value[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.stable_bits_value["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PFeedForward.stable-bits-value",this$);
}
}
}
});

/**
 * Given the index of an output bit from this source, return the
 *  corresponding local cell id as [col ci] where col is the column
 *  index. If the source is a sense, returns [i].
 */
org.nfrac.comportex.protocols.source_of_bit = (function org$nfrac$comportex$protocols$source_of_bit(this$,i){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PFeedForward$source_of_bit$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PFeedForward$source_of_bit$arity$2(this$,i);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.source_of_bit[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,i) : m__6809__auto__.call(null,this$,i));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.source_of_bit["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,i) : m__6809__auto____$1.call(null,this$,i));
} else {
throw cljs.core.missing_protocol("PFeedForward.source-of-bit",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PFeedBack = function(){};

/**
 * The set of indices of all winner cells.
 */
org.nfrac.comportex.protocols.wc_bits_value = (function org$nfrac$comportex$protocols$wc_bits_value(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PFeedBack$wc_bits_value$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PFeedBack$wc_bits_value$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.wc_bits_value[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.wc_bits_value["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PFeedBack.wc-bits-value",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PFeedForwardMotor = function(){};

org.nfrac.comportex.protocols.ff_motor_topology = (function org$nfrac$comportex$protocols$ff_motor_topology(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PFeedForwardMotor$ff_motor_topology$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PFeedForwardMotor$ff_motor_topology$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.ff_motor_topology[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.ff_motor_topology["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PFeedForwardMotor.ff-motor-topology",this$);
}
}
}
});

org.nfrac.comportex.protocols.motor_bits_value = (function org$nfrac$comportex$protocols$motor_bits_value(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PFeedForwardMotor$motor_bits_value$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PFeedForwardMotor$motor_bits_value$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.motor_bits_value[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.motor_bits_value["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PFeedForwardMotor.motor-bits-value",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PLayerOfCells = function(){};

org.nfrac.comportex.protocols.layer_activate = (function org$nfrac$comportex$protocols$layer_activate(this$,ff_bits,stable_ff_bits){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_activate$arity$3 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_activate$arity$3(this$,ff_bits,stable_ff_bits);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.layer_activate[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,ff_bits,stable_ff_bits) : m__6809__auto__.call(null,this$,ff_bits,stable_ff_bits));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.layer_activate["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,ff_bits,stable_ff_bits) : m__6809__auto____$1.call(null,this$,ff_bits,stable_ff_bits));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.layer-activate",this$);
}
}
}
});

org.nfrac.comportex.protocols.layer_learn = (function org$nfrac$comportex$protocols$layer_learn(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_learn$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_learn$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.layer_learn[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.layer_learn["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.layer-learn",this$);
}
}
}
});

org.nfrac.comportex.protocols.layer_depolarise = (function org$nfrac$comportex$protocols$layer_depolarise(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_depolarise$arity$4 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_depolarise$arity$4(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.layer_depolarise[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$4(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits) : m__6809__auto__.call(null,this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.layer_depolarise["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4(this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits) : m__6809__auto____$1.call(null,this$,distal_ff_bits,apical_fb_bits,apical_fb_wc_bits));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.layer-depolarise",this$);
}
}
}
});

/**
 * Number of cells per column.
 */
org.nfrac.comportex.protocols.layer_depth = (function org$nfrac$comportex$protocols$layer_depth(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_depth$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$layer_depth$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.layer_depth[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.layer_depth["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.layer-depth",this$);
}
}
}
});

/**
 * The set of bursting column ids.
 */
org.nfrac.comportex.protocols.bursting_columns = (function org$nfrac$comportex$protocols$bursting_columns(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$bursting_columns$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$bursting_columns$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.bursting_columns[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.bursting_columns["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.bursting-columns",this$);
}
}
}
});

/**
 * The set of active column ids.
 */
org.nfrac.comportex.protocols.active_columns = (function org$nfrac$comportex$protocols$active_columns(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$active_columns$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$active_columns$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.active_columns[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.active_columns["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.active-columns",this$);
}
}
}
});

/**
 * The set of active cell ids.
 */
org.nfrac.comportex.protocols.active_cells = (function org$nfrac$comportex$protocols$active_cells(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$active_cells$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$active_cells$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.active_cells[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.active_cells["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.active-cells",this$);
}
}
}
});

/**
 * The set of winning cell ids, one in each active column. These are
 *  only _learning_ cells when they turn on, but are always
 *  _learnable_.
 */
org.nfrac.comportex.protocols.winner_cells = (function org$nfrac$comportex$protocols$winner_cells(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$winner_cells$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$winner_cells$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.winner_cells[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.winner_cells["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.winner-cells",this$);
}
}
}
});

/**
 * The set of predictive cell ids derived from the current active
 *  cells. If the depolarise phase has not been applied yet, returns
 *  nil.
 */
org.nfrac.comportex.protocols.predictive_cells = (function org$nfrac$comportex$protocols$predictive_cells(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$predictive_cells$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$predictive_cells$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.predictive_cells[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.predictive_cells["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.predictive-cells",this$);
}
}
}
});

/**
 * The set of predictive cell ids from the previous timestep,
 *  i.e. their prediction can be compared to the current active
 *  cells.
 */
org.nfrac.comportex.protocols.prior_predictive_cells = (function org$nfrac$comportex$protocols$prior_predictive_cells(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PLayerOfCells$prior_predictive_cells$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PLayerOfCells$prior_predictive_cells$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.prior_predictive_cells[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.prior_predictive_cells["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PLayerOfCells.prior-predictive-cells",this$);
}
}
}
});


/**
 * The synaptic connections from a set of sources to a set of targets.
 * Synapses have an associated permanence value between 0 and 1; above
 * some permanence level they are defined to be connected.
 * @interface
 */
org.nfrac.comportex.protocols.PSynapseGraph = function(){};

/**
 * All synapses to the target. A map from source ids to permanences.
 */
org.nfrac.comportex.protocols.in_synapses = (function org$nfrac$comportex$protocols$in_synapses(this$,target_id){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSynapseGraph$in_synapses$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PSynapseGraph$in_synapses$arity$2(this$,target_id);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.in_synapses[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,target_id) : m__6809__auto__.call(null,this$,target_id));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.in_synapses["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,target_id) : m__6809__auto____$1.call(null,this$,target_id));
} else {
throw cljs.core.missing_protocol("PSynapseGraph.in-synapses",this$);
}
}
}
});

/**
 * The collection of source ids actually connected to target id.
 */
org.nfrac.comportex.protocols.sources_connected_to = (function org$nfrac$comportex$protocols$sources_connected_to(this$,target_id){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSynapseGraph$sources_connected_to$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PSynapseGraph$sources_connected_to$arity$2(this$,target_id);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.sources_connected_to[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,target_id) : m__6809__auto__.call(null,this$,target_id));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.sources_connected_to["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,target_id) : m__6809__auto____$1.call(null,this$,target_id));
} else {
throw cljs.core.missing_protocol("PSynapseGraph.sources-connected-to",this$);
}
}
}
});

/**
 * The collection of target ids actually connected from source id.
 */
org.nfrac.comportex.protocols.targets_connected_from = (function org$nfrac$comportex$protocols$targets_connected_from(this$,source_id){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSynapseGraph$targets_connected_from$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PSynapseGraph$targets_connected_from$arity$2(this$,source_id);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.targets_connected_from[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,source_id) : m__6809__auto__.call(null,this$,source_id));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.targets_connected_from["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,source_id) : m__6809__auto____$1.call(null,this$,source_id));
} else {
throw cljs.core.missing_protocol("PSynapseGraph.targets-connected-from",this$);
}
}
}
});

/**
 * Computes a map of target ids to their degree of excitation -- the
 *  number of sources in `active-sources` they are connected to -- excluding
 *  any below `stimulus-threshold`.
 */
org.nfrac.comportex.protocols.excitations = (function org$nfrac$comportex$protocols$excitations(this$,active_sources,stimulus_threshold){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSynapseGraph$excitations$arity$3 == null)))){
return this$.org$nfrac$comportex$protocols$PSynapseGraph$excitations$arity$3(this$,active_sources,stimulus_threshold);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.excitations[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,active_sources,stimulus_threshold) : m__6809__auto__.call(null,this$,active_sources,stimulus_threshold));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.excitations["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,active_sources,stimulus_threshold) : m__6809__auto____$1.call(null,this$,active_sources,stimulus_threshold));
} else {
throw cljs.core.missing_protocol("PSynapseGraph.excitations",this$);
}
}
}
});

/**
 * Applies learning updates to a batch of targets. `seg-updates` is
 *  a sequence of SegUpdate records, one for each target dendrite
 *  segment.
 */
org.nfrac.comportex.protocols.bulk_learn = (function org$nfrac$comportex$protocols$bulk_learn(this$,seg_updates,active_sources,pinc,pdec,pinit){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSynapseGraph$bulk_learn$arity$6 == null)))){
return this$.org$nfrac$comportex$protocols$PSynapseGraph$bulk_learn$arity$6(this$,seg_updates,active_sources,pinc,pdec,pinit);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.bulk_learn[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$6 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$6(this$,seg_updates,active_sources,pinc,pdec,pinit) : m__6809__auto__.call(null,this$,seg_updates,active_sources,pinc,pdec,pinit));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.bulk_learn["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$6 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$6(this$,seg_updates,active_sources,pinc,pdec,pinit) : m__6809__auto____$1.call(null,this$,seg_updates,active_sources,pinc,pdec,pinit));
} else {
throw cljs.core.missing_protocol("PSynapseGraph.bulk-learn",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PSegments = function(){};

/**
 * A vector of segments on the cell, each being a synapse map.
 */
org.nfrac.comportex.protocols.cell_segments = (function org$nfrac$comportex$protocols$cell_segments(this$,cell_id){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSegments$cell_segments$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PSegments$cell_segments$arity$2(this$,cell_id);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.cell_segments[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,cell_id) : m__6809__auto__.call(null,this$,cell_id));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.cell_segments["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,cell_id) : m__6809__auto____$1.call(null,this$,cell_id));
} else {
throw cljs.core.missing_protocol("PSegments.cell-segments",this$);
}
}
}
});


/**
 * Sense nodes need to extend this together with PFeedForward.
 * @interface
 */
org.nfrac.comportex.protocols.PSense = function(){};

org.nfrac.comportex.protocols.sense_activate = (function org$nfrac$comportex$protocols$sense_activate(this$,bits){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSense$sense_activate$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PSense$sense_activate$arity$2(this$,bits);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.sense_activate[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,bits) : m__6809__auto__.call(null,this$,bits));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.sense_activate["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,bits) : m__6809__auto____$1.call(null,this$,bits));
} else {
throw cljs.core.missing_protocol("PSense.sense-activate",this$);
}
}
}
});


/**
 * Pulls out a value according to some pattern, like a path or lens.
 *   Should be serializable. A Sensor is defined as [Selector Encoder].
 * @interface
 */
org.nfrac.comportex.protocols.PSelector = function(){};

/**
 * Extracts a value from `state` according to some configured pattern. A
 *  simple example is a lookup by keyword in a map.
 */
org.nfrac.comportex.protocols.extract = (function org$nfrac$comportex$protocols$extract(this$,state){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PSelector$extract$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PSelector$extract$arity$2(this$,state);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.extract[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,state) : m__6809__auto__.call(null,this$,state));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.extract["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,state) : m__6809__auto____$1.call(null,this$,state));
} else {
throw cljs.core.missing_protocol("PSelector.extract",this$);
}
}
}
});


/**
 * Encoders need to extend this together with PTopological.
 * @interface
 */
org.nfrac.comportex.protocols.PEncoder = function(){};

/**
 * Encodes `x` as a collection of distinct integers which are the on-bits.
 */
org.nfrac.comportex.protocols.encode = (function org$nfrac$comportex$protocols$encode(this$,x){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PEncoder$encode$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PEncoder$encode$arity$2(this$,x);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.encode[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,x) : m__6809__auto__.call(null,this$,x));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.encode["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,x) : m__6809__auto____$1.call(null,this$,x));
} else {
throw cljs.core.missing_protocol("PEncoder.encode",this$);
}
}
}
});

/**
 * Finds `n` domain values matching the given bit set in a sequence
 *   of maps with keys `:value`, `:votes-frac`, `:votes-per-bit`,
 *   `:bit-coverage`, `:bit-precision`, ordered by votes fraction
 *   decreasing. The argument `bit-votes` is a map from encoded bit
 *   index to a number of votes, typically the number of synapse
 *   connections from predictive cells.
 */
org.nfrac.comportex.protocols.decode = (function org$nfrac$comportex$protocols$decode(this$,bit_votes,n){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PEncoder$decode$arity$3 == null)))){
return this$.org$nfrac$comportex$protocols$PEncoder$decode$arity$3(this$,bit_votes,n);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.decode[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,bit_votes,n) : m__6809__auto__.call(null,this$,bit_votes,n));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.decode["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,bit_votes,n) : m__6809__auto____$1.call(null,this$,bit_votes,n));
} else {
throw cljs.core.missing_protocol("PEncoder.decode",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PRestartable = function(){};

/**
 * Returns this model (or model component) reverted to its initial
 *  state prior to any learning.
 */
org.nfrac.comportex.protocols.restart = (function org$nfrac$comportex$protocols$restart(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PRestartable$restart$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PRestartable$restart$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.restart[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.restart["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PRestartable.restart",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PInterruptable = function(){};

/**
 * Returns this model (or model component) without its current
 *  sequence state, forcing the following input to be treated as a new
 *  sequence. `mode` can be
 * 
 *  * :tm, cancels any distal predictions and prevents learning
 *    lateral/distal connections.
 *  * :fb, cancels any feedback predictions and prevents learning
 *    connections on apical dendrites.
 *  * :syns, cancels any continuing stable synapses used for temporal
 *    pooling in any higher layers (not `this` layer).
 *  * :winners, allows new winner cells to be chosen in continuing
 *    columns.
 */
org.nfrac.comportex.protocols.break$ = (function org$nfrac$comportex$protocols$break(this$,mode){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PInterruptable$break$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PInterruptable$break$arity$2(this$,mode);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.break$[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,mode) : m__6809__auto__.call(null,this$,mode));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.break$["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,mode) : m__6809__auto____$1.call(null,this$,mode));
} else {
throw cljs.core.missing_protocol("PInterruptable.break",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PTemporal = function(){};

org.nfrac.comportex.protocols.timestep = (function org$nfrac$comportex$protocols$timestep(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PTemporal$timestep$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PTemporal$timestep$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.timestep[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.timestep["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PTemporal.timestep",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PParameterised = function(){};

/**
 * A parameter set as map with keyword keys.
 */
org.nfrac.comportex.protocols.params = (function org$nfrac$comportex$protocols$params(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PParameterised$params$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PParameterised$params$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.params[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.params["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PParameterised.params",this$);
}
}
}
});


/**
 * @interface
 */
org.nfrac.comportex.protocols.PTopological = function(){};

org.nfrac.comportex.protocols.topology = (function org$nfrac$comportex$protocols$topology(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PTopological$topology$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PTopological$topology$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.topology[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.topology["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PTopological.topology",this$);
}
}
}
});


/**
 * Operating on a regular grid of certain dimensions, where each
 * coordinate is an n-tuple vector---or integer for 1D---and also has
 * a unique integer index.
 * @interface
 */
org.nfrac.comportex.protocols.PTopology = function(){};

org.nfrac.comportex.protocols.dimensions = (function org$nfrac$comportex$protocols$dimensions(this$){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PTopology$dimensions$arity$1 == null)))){
return this$.org$nfrac$comportex$protocols$PTopology$dimensions$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.dimensions[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.dimensions["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PTopology.dimensions",this$);
}
}
}
});

org.nfrac.comportex.protocols.coordinates_of_index = (function org$nfrac$comportex$protocols$coordinates_of_index(this$,idx){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PTopology$coordinates_of_index$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PTopology$coordinates_of_index$arity$2(this$,idx);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.coordinates_of_index[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,idx) : m__6809__auto__.call(null,this$,idx));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.coordinates_of_index["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,idx) : m__6809__auto____$1.call(null,this$,idx));
} else {
throw cljs.core.missing_protocol("PTopology.coordinates-of-index",this$);
}
}
}
});

org.nfrac.comportex.protocols.index_of_coordinates = (function org$nfrac$comportex$protocols$index_of_coordinates(this$,coord){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PTopology$index_of_coordinates$arity$2 == null)))){
return this$.org$nfrac$comportex$protocols$PTopology$index_of_coordinates$arity$2(this$,coord);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.index_of_coordinates[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,coord) : m__6809__auto__.call(null,this$,coord));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.index_of_coordinates["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,coord) : m__6809__auto____$1.call(null,this$,coord));
} else {
throw cljs.core.missing_protocol("PTopology.index-of-coordinates",this$);
}
}
}
});

org.nfrac.comportex.protocols.neighbours_STAR_ = (function org$nfrac$comportex$protocols$neighbours_STAR_(this$,coord,outer_r,inner_r){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PTopology$neighbours_STAR_$arity$4 == null)))){
return this$.org$nfrac$comportex$protocols$PTopology$neighbours_STAR_$arity$4(this$,coord,outer_r,inner_r);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.neighbours_STAR_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$4(this$,coord,outer_r,inner_r) : m__6809__auto__.call(null,this$,coord,outer_r,inner_r));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.neighbours_STAR_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4(this$,coord,outer_r,inner_r) : m__6809__auto____$1.call(null,this$,coord,outer_r,inner_r));
} else {
throw cljs.core.missing_protocol("PTopology.neighbours*",this$);
}
}
}
});

org.nfrac.comportex.protocols.coord_distance = (function org$nfrac$comportex$protocols$coord_distance(this$,coord_a,coord_b){
if((!((this$ == null))) && (!((this$.org$nfrac$comportex$protocols$PTopology$coord_distance$arity$3 == null)))){
return this$.org$nfrac$comportex$protocols$PTopology$coord_distance$arity$3(this$,coord_a,coord_b);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.nfrac.comportex.protocols.coord_distance[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,coord_a,coord_b) : m__6809__auto__.call(null,this$,coord_a,coord_b));
} else {
var m__6809__auto____$1 = (org.nfrac.comportex.protocols.coord_distance["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,coord_a,coord_b) : m__6809__auto____$1.call(null,this$,coord_a,coord_b));
} else {
throw cljs.core.missing_protocol("PTopology.coord-distance",this$);
}
}
}
});

/**
 * The total number of elements indexed in the topology.
 */
org.nfrac.comportex.protocols.size = (function org$nfrac$comportex$protocols$size(topo){
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core._STAR_,org.nfrac.comportex.protocols.dimensions(topo));
});
/**
 * The dimensions of a PTopological as an n-tuple vector.
 */
org.nfrac.comportex.protocols.dims_of = (function org$nfrac$comportex$protocols$dims_of(x){
return org.nfrac.comportex.protocols.dimensions(org.nfrac.comportex.protocols.topology(x));
});
/**
 * The total number of elements in a PTopological.
 */
org.nfrac.comportex.protocols.size_of = (function org$nfrac$comportex$protocols$size_of(x){
return org.nfrac.comportex.protocols.size(org.nfrac.comportex.protocols.topology(x));
});
/**
 * Returns the coordinates away from `coord` at distances
 *   `inner-r` (exclusive) out to `outer-r` (inclusive) .
 */
org.nfrac.comportex.protocols.neighbours = (function org$nfrac$comportex$protocols$neighbours(var_args){
var args36260 = [];
var len__7211__auto___36263 = arguments.length;
var i__7212__auto___36264 = (0);
while(true){
if((i__7212__auto___36264 < len__7211__auto___36263)){
args36260.push((arguments[i__7212__auto___36264]));

var G__36265 = (i__7212__auto___36264 + (1));
i__7212__auto___36264 = G__36265;
continue;
} else {
}
break;
}

var G__36262 = args36260.length;
switch (G__36262) {
case 3:
return org.nfrac.comportex.protocols.neighbours.cljs$core$IFn$_invoke$arity$3((arguments[(0)]),(arguments[(1)]),(arguments[(2)]));

break;
case 4:
return org.nfrac.comportex.protocols.neighbours.cljs$core$IFn$_invoke$arity$4((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args36260.length)].join('')));

}
});

org.nfrac.comportex.protocols.neighbours.cljs$core$IFn$_invoke$arity$3 = (function (topo,coord,radius){
return org.nfrac.comportex.protocols.neighbours_STAR_(topo,coord,radius,(0));
});

org.nfrac.comportex.protocols.neighbours.cljs$core$IFn$_invoke$arity$4 = (function (topo,coord,outer_r,inner_r){
return org.nfrac.comportex.protocols.neighbours_STAR_(topo,coord,outer_r,inner_r);
});

org.nfrac.comportex.protocols.neighbours.cljs$lang$maxFixedArity = 4;
/**
 * Same as `neighbours` but taking and returning indices instead of
 * coordinates.
 */
org.nfrac.comportex.protocols.neighbours_indices = (function org$nfrac$comportex$protocols$neighbours_indices(var_args){
var args36267 = [];
var len__7211__auto___36270 = arguments.length;
var i__7212__auto___36271 = (0);
while(true){
if((i__7212__auto___36271 < len__7211__auto___36270)){
args36267.push((arguments[i__7212__auto___36271]));

var G__36272 = (i__7212__auto___36271 + (1));
i__7212__auto___36271 = G__36272;
continue;
} else {
}
break;
}

var G__36269 = args36267.length;
switch (G__36269) {
case 3:
return org.nfrac.comportex.protocols.neighbours_indices.cljs$core$IFn$_invoke$arity$3((arguments[(0)]),(arguments[(1)]),(arguments[(2)]));

break;
case 4:
return org.nfrac.comportex.protocols.neighbours_indices.cljs$core$IFn$_invoke$arity$4((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args36267.length)].join('')));

}
});

org.nfrac.comportex.protocols.neighbours_indices.cljs$core$IFn$_invoke$arity$3 = (function (topo,idx,radius){
return org.nfrac.comportex.protocols.neighbours_indices.cljs$core$IFn$_invoke$arity$4(topo,idx,radius,(0));
});

org.nfrac.comportex.protocols.neighbours_indices.cljs$core$IFn$_invoke$arity$4 = (function (topo,idx,outer_r,inner_r){
return cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.partial.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.protocols.index_of_coordinates,topo),org.nfrac.comportex.protocols.neighbours_STAR_(topo,org.nfrac.comportex.protocols.coordinates_of_index(topo,idx),outer_r,inner_r));
});

org.nfrac.comportex.protocols.neighbours_indices.cljs$lang$maxFixedArity = 4;
