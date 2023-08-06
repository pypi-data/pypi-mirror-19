// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.viz_layouts');
goog.require('cljs.core');
goog.require('monet.canvas');
goog.require('tailrecursion.priority_map');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.topology');

/**
 * @interface
 */
org.numenta.sanity.viz_layouts.PBox = function(){};

/**
 * Returns `{:x :y :w :h}` defining bounding box from top left.
 */
org.numenta.sanity.viz_layouts.layout_bounds = (function org$numenta$sanity$viz_layouts$layout_bounds(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PBox$layout_bounds$arity$1 == null)))){
return this$.org$numenta$sanity$viz_layouts$PBox$layout_bounds$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.layout_bounds[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.layout_bounds["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PBox.layout-bounds",this$);
}
}
}
});


/**
 * @interface
 */
org.numenta.sanity.viz_layouts.PArrayLayout = function(){};

/**
 * Returns [x y] pixel coordinates for top left of time offset dt.
 */
org.numenta.sanity.viz_layouts.origin_px_topleft = (function org$numenta$sanity$viz_layouts$origin_px_topleft(this$,dt){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$origin_px_topleft$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$origin_px_topleft$arity$2(this$,dt);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.origin_px_topleft[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,dt) : m__6809__auto__.call(null,this$,dt));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.origin_px_topleft["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,dt) : m__6809__auto____$1.call(null,this$,dt));
} else {
throw cljs.core.missing_protocol("PArrayLayout.origin-px-topleft",this$);
}
}
}
});

/**
 * Returns `{:x :y :w :h}` defining local bounding box relative to dt origin.
 */
org.numenta.sanity.viz_layouts.local_dt_bounds = (function org$numenta$sanity$viz_layouts$local_dt_bounds(this$,dt){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$local_dt_bounds$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$local_dt_bounds$arity$2(this$,dt);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.local_dt_bounds[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,dt) : m__6809__auto__.call(null,this$,dt));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.local_dt_bounds["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,dt) : m__6809__auto____$1.call(null,this$,dt));
} else {
throw cljs.core.missing_protocol("PArrayLayout.local-dt-bounds",this$);
}
}
}
});

/**
 * Returns [x y] pixel coordinates for id relative to the dt origin.
 */
org.numenta.sanity.viz_layouts.local_px_topleft = (function org$numenta$sanity$viz_layouts$local_px_topleft(this$,id){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$local_px_topleft$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$local_px_topleft$arity$2(this$,id);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.local_px_topleft[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,id) : m__6809__auto__.call(null,this$,id));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.local_px_topleft["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,id) : m__6809__auto____$1.call(null,this$,id));
} else {
throw cljs.core.missing_protocol("PArrayLayout.local-px-topleft",this$);
}
}
}
});

/**
 * The size [w h] in pixels of each drawn array element.
 */
org.numenta.sanity.viz_layouts.element_size_px = (function org$numenta$sanity$viz_layouts$element_size_px(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$element_size_px$arity$1 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$element_size_px$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.element_size_px[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.element_size_px["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PArrayLayout.element-size-px",this$);
}
}
}
});

/**
 * Current scroll position, giving the first element index visible on screen.
 */
org.numenta.sanity.viz_layouts.scroll_position = (function org$numenta$sanity$viz_layouts$scroll_position(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$scroll_position$arity$1 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$scroll_position$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.scroll_position[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.scroll_position["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PArrayLayout.scroll-position",this$);
}
}
}
});

/**
 * Updates the layout with scroll position adjusted up or down one page.
 */
org.numenta.sanity.viz_layouts.scroll = (function org$numenta$sanity$viz_layouts$scroll(this$,down_QMARK_){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$scroll$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$scroll$arity$2(this$,down_QMARK_);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.scroll[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,down_QMARK_) : m__6809__auto__.call(null,this$,down_QMARK_));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.scroll["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,down_QMARK_) : m__6809__auto____$1.call(null,this$,down_QMARK_));
} else {
throw cljs.core.missing_protocol("PArrayLayout.scroll",this$);
}
}
}
});

/**
 * Returns the total number of ids
 */
org.numenta.sanity.viz_layouts.ids_count = (function org$numenta$sanity$viz_layouts$ids_count(_){
if((!((_ == null))) && (!((_.org$numenta$sanity$viz_layouts$PArrayLayout$ids_count$arity$1 == null)))){
return _.org$numenta$sanity$viz_layouts$PArrayLayout$ids_count$arity$1(_);
} else {
var x__6808__auto__ = (((_ == null))?null:_);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.ids_count[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(_) : m__6809__auto__.call(null,_));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.ids_count["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(_) : m__6809__auto____$1.call(null,_));
} else {
throw cljs.core.missing_protocol("PArrayLayout.ids-count",_);
}
}
}
});

/**
 * Returns the number of ids onscreen in constant time
 */
org.numenta.sanity.viz_layouts.ids_onscreen_count = (function org$numenta$sanity$viz_layouts$ids_onscreen_count(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen_count$arity$1 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen_count$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.ids_onscreen_count[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.ids_onscreen_count["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PArrayLayout.ids-onscreen-count",this$);
}
}
}
});

/**
 * Sequence of element ids per timestep currently drawn in the layout.
 */
org.numenta.sanity.viz_layouts.ids_onscreen = (function org$numenta$sanity$viz_layouts$ids_onscreen(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen$arity$1 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.ids_onscreen[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.ids_onscreen["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PArrayLayout.ids-onscreen",this$);
}
}
}
});

/**
 * Checks whether the element id is currently drawn in the layout.
 */
org.numenta.sanity.viz_layouts.id_onscreen_QMARK_ = (function org$numenta$sanity$viz_layouts$id_onscreen_QMARK_(this$,id){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$id_onscreen_QMARK_$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$id_onscreen_QMARK_$arity$2(this$,id);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.id_onscreen_QMARK_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,id) : m__6809__auto__.call(null,this$,id));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.id_onscreen_QMARK_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,id) : m__6809__auto____$1.call(null,this$,id));
} else {
throw cljs.core.missing_protocol("PArrayLayout.id-onscreen?",this$);
}
}
}
});

/**
 * Returns [dt id] for the [x y] pixel coordinates, or null.
 */
org.numenta.sanity.viz_layouts.clicked_id = (function org$numenta$sanity$viz_layouts$clicked_id(this$,x,y){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$clicked_id$arity$3 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$clicked_id$arity$3(this$,x,y);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.clicked_id[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,x,y) : m__6809__auto__.call(null,this$,x,y));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.clicked_id["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,x,y) : m__6809__auto____$1.call(null,this$,x,y));
} else {
throw cljs.core.missing_protocol("PArrayLayout.clicked-id",this$);
}
}
}
});

/**
 * Draws the element in dt-local coordinates. Does not stroke or fill.
 */
org.numenta.sanity.viz_layouts.draw_element = (function org$numenta$sanity$viz_layouts$draw_element(this$,ctx,id){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PArrayLayout$draw_element$arity$3 == null)))){
return this$.org$numenta$sanity$viz_layouts$PArrayLayout$draw_element$arity$3(this$,ctx,id);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.draw_element[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,ctx,id) : m__6809__auto__.call(null,this$,ctx,id));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.draw_element["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,ctx,id) : m__6809__auto____$1.call(null,this$,ctx,id));
} else {
throw cljs.core.missing_protocol("PArrayLayout.draw-element",this$);
}
}
}
});

org.numenta.sanity.viz_layouts.right_px = (function org$numenta$sanity$viz_layouts$right_px(this$){
var b = org.numenta.sanity.viz_layouts.layout_bounds(this$);
return (cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(b) + cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(b));
});
/**
 * Returns pixel coordinates on the canvas `[x y]` for the
 * center of an input element `id` at time delay `dt`.
 */
org.numenta.sanity.viz_layouts.element_xy = (function org$numenta$sanity$viz_layouts$element_xy(lay,id,dt){
var vec__47087 = org.numenta.sanity.viz_layouts.element_size_px(lay);
var w = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47087,(0),null);
var h = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47087,(1),null);
var vec__47088 = org.numenta.sanity.viz_layouts.origin_px_topleft(lay,dt);
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47088,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47088,(1),null);
var vec__47089 = org.numenta.sanity.viz_layouts.local_px_topleft(lay,id);
var lx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47089,(0),null);
var ly = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47089,(1),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [((x + lx) + (w * 0.5)),((y + ly) + (h * 0.5))], null);
});
/**
 * Fills all elements with the given ids (in a single path if
 *   possible). For efficiency, skips any ids which are currently
 *   offscreen.
 */
org.numenta.sanity.viz_layouts.fill_elements = (function org$numenta$sanity$viz_layouts$fill_elements(lay,ctx,ids){
var one_d_QMARK_ = ((1) === cljs.core.count(org.nfrac.comportex.protocols.dims_of(lay)));
monet.canvas.begin_path(ctx);

var seq__47096_47102 = cljs.core.seq(ids);
var chunk__47098_47103 = null;
var count__47099_47104 = (0);
var i__47100_47105 = (0);
while(true){
if((i__47100_47105 < count__47099_47104)){
var id_47106 = chunk__47098_47103.cljs$core$IIndexed$_nth$arity$2(null,i__47100_47105);
if(cljs.core.truth_(org.numenta.sanity.viz_layouts.id_onscreen_QMARK_(lay,id_47106))){
org.numenta.sanity.viz_layouts.draw_element(lay,ctx,id_47106);

if(one_d_QMARK_){
} else {
monet.canvas.fill(ctx);

monet.canvas.begin_path(ctx);
}

var G__47107 = seq__47096_47102;
var G__47108 = chunk__47098_47103;
var G__47109 = count__47099_47104;
var G__47110 = (i__47100_47105 + (1));
seq__47096_47102 = G__47107;
chunk__47098_47103 = G__47108;
count__47099_47104 = G__47109;
i__47100_47105 = G__47110;
continue;
} else {
var G__47111 = seq__47096_47102;
var G__47112 = chunk__47098_47103;
var G__47113 = count__47099_47104;
var G__47114 = (i__47100_47105 + (1));
seq__47096_47102 = G__47111;
chunk__47098_47103 = G__47112;
count__47099_47104 = G__47113;
i__47100_47105 = G__47114;
continue;
}
} else {
var temp__4657__auto___47115 = cljs.core.seq(seq__47096_47102);
if(temp__4657__auto___47115){
var seq__47096_47116__$1 = temp__4657__auto___47115;
if(cljs.core.chunked_seq_QMARK_(seq__47096_47116__$1)){
var c__6956__auto___47117 = cljs.core.chunk_first(seq__47096_47116__$1);
var G__47118 = cljs.core.chunk_rest(seq__47096_47116__$1);
var G__47119 = c__6956__auto___47117;
var G__47120 = cljs.core.count(c__6956__auto___47117);
var G__47121 = (0);
seq__47096_47102 = G__47118;
chunk__47098_47103 = G__47119;
count__47099_47104 = G__47120;
i__47100_47105 = G__47121;
continue;
} else {
var id_47122 = cljs.core.first(seq__47096_47116__$1);
if(cljs.core.truth_(org.numenta.sanity.viz_layouts.id_onscreen_QMARK_(lay,id_47122))){
org.numenta.sanity.viz_layouts.draw_element(lay,ctx,id_47122);

if(one_d_QMARK_){
} else {
monet.canvas.fill(ctx);

monet.canvas.begin_path(ctx);
}

var G__47123 = cljs.core.next(seq__47096_47116__$1);
var G__47124 = null;
var G__47125 = (0);
var G__47126 = (0);
seq__47096_47102 = G__47123;
chunk__47098_47103 = G__47124;
count__47099_47104 = G__47125;
i__47100_47105 = G__47126;
continue;
} else {
var G__47127 = cljs.core.next(seq__47096_47116__$1);
var G__47128 = null;
var G__47129 = (0);
var G__47130 = (0);
seq__47096_47102 = G__47127;
chunk__47098_47103 = G__47128;
count__47099_47104 = G__47129;
i__47100_47105 = G__47130;
continue;
}
}
} else {
}
}
break;
}

if(one_d_QMARK_){
monet.canvas.fill(ctx);
} else {
}

return ctx;
});
/**
 * Groups the map `id-styles` by key, each key being a style value.
 * For each such group, calls `set-style` with the value and then
 * fills the group of elements.
 */
org.numenta.sanity.viz_layouts.group_and_fill_elements = (function org$numenta$sanity$viz_layouts$group_and_fill_elements(lay,ctx,id_styles,set_style){
monet.canvas.save(ctx);

var seq__47137_47143 = cljs.core.seq(cljs.core.group_by(id_styles,cljs.core.keys(id_styles)));
var chunk__47138_47144 = null;
var count__47139_47145 = (0);
var i__47140_47146 = (0);
while(true){
if((i__47140_47146 < count__47139_47145)){
var vec__47141_47147 = chunk__47138_47144.cljs$core$IIndexed$_nth$arity$2(null,i__47140_47146);
var style_47148 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47141_47147,(0),null);
var ids_47149 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47141_47147,(1),null);
(set_style.cljs$core$IFn$_invoke$arity$2 ? set_style.cljs$core$IFn$_invoke$arity$2(ctx,style_47148) : set_style.call(null,ctx,style_47148));

org.numenta.sanity.viz_layouts.fill_elements(lay,ctx,ids_47149);

monet.canvas.fill(ctx);

var G__47150 = seq__47137_47143;
var G__47151 = chunk__47138_47144;
var G__47152 = count__47139_47145;
var G__47153 = (i__47140_47146 + (1));
seq__47137_47143 = G__47150;
chunk__47138_47144 = G__47151;
count__47139_47145 = G__47152;
i__47140_47146 = G__47153;
continue;
} else {
var temp__4657__auto___47154 = cljs.core.seq(seq__47137_47143);
if(temp__4657__auto___47154){
var seq__47137_47155__$1 = temp__4657__auto___47154;
if(cljs.core.chunked_seq_QMARK_(seq__47137_47155__$1)){
var c__6956__auto___47156 = cljs.core.chunk_first(seq__47137_47155__$1);
var G__47157 = cljs.core.chunk_rest(seq__47137_47155__$1);
var G__47158 = c__6956__auto___47156;
var G__47159 = cljs.core.count(c__6956__auto___47156);
var G__47160 = (0);
seq__47137_47143 = G__47157;
chunk__47138_47144 = G__47158;
count__47139_47145 = G__47159;
i__47140_47146 = G__47160;
continue;
} else {
var vec__47142_47161 = cljs.core.first(seq__47137_47155__$1);
var style_47162 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47142_47161,(0),null);
var ids_47163 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47142_47161,(1),null);
(set_style.cljs$core$IFn$_invoke$arity$2 ? set_style.cljs$core$IFn$_invoke$arity$2(ctx,style_47162) : set_style.call(null,ctx,style_47162));

org.numenta.sanity.viz_layouts.fill_elements(lay,ctx,ids_47163);

monet.canvas.fill(ctx);

var G__47164 = cljs.core.next(seq__47137_47155__$1);
var G__47165 = null;
var G__47166 = (0);
var G__47167 = (0);
seq__47137_47143 = G__47164;
chunk__47138_47144 = G__47165;
count__47139_47145 = G__47166;
i__47140_47146 = G__47167;
continue;
}
} else {
}
}
break;
}

monet.canvas.restore(ctx);

return ctx;
});
org.numenta.sanity.viz_layouts.circle = (function org$numenta$sanity$viz_layouts$circle(ctx,x,y,r){
return ctx.arc(x,y,r,(0),(Math.PI * (2)),true);
});
org.numenta.sanity.viz_layouts.circle_from_bounds = (function org$numenta$sanity$viz_layouts$circle_from_bounds(ctx,x,y,w){
var r = (w * 0.5);
return org.numenta.sanity.viz_layouts.circle(ctx,(x + r),(y + r),r);
});
org.numenta.sanity.viz_layouts.extra_px_for_highlight = (4);
org.numenta.sanity.viz_layouts.highlight_rect = (function org$numenta$sanity$viz_layouts$highlight_rect(ctx,rect,color){
var G__47169 = ctx;
monet.canvas.stroke_style(G__47169,color);

monet.canvas.stroke_width(G__47169,(3));

monet.canvas.stroke_rect(G__47169,rect);

monet.canvas.stroke_style(G__47169,"black");

monet.canvas.stroke_width(G__47169,0.75);

monet.canvas.stroke_rect(G__47169,rect);

return G__47169;
});
/**
 * Draws highlight around the whole layout in global coordinates.
 */
org.numenta.sanity.viz_layouts.highlight_layer = (function org$numenta$sanity$viz_layouts$highlight_layer(lay,ctx,color){
var bb = org.numenta.sanity.viz_layouts.layout_bounds(lay);
var scroll_off = (((org.numenta.sanity.viz_layouts.scroll_position(lay) > (0)))?(50):(0));
return org.numenta.sanity.viz_layouts.highlight_rect(ctx,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(bb) - (1)),cljs.core.cst$kw$y,((cljs.core.cst$kw$y.cljs$core$IFn$_invoke$arity$1(bb) - (1)) - scroll_off),cljs.core.cst$kw$w,(cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(bb) + (2)),cljs.core.cst$kw$h,((cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(bb) + (2)) + scroll_off)], null),color);
});
/**
 * Draws highlight on the time offset dt in global coordinates.
 */
org.numenta.sanity.viz_layouts.highlight_dt = (function org$numenta$sanity$viz_layouts$highlight_dt(lay,ctx,dt,color){
var vec__47171 = org.numenta.sanity.viz_layouts.origin_px_topleft(lay,dt);
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47171,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47171,(1),null);
var bb = org.numenta.sanity.viz_layouts.local_dt_bounds(lay,dt);
var scroll_off = (((org.numenta.sanity.viz_layouts.scroll_position(lay) > (0)))?(50):(0));
return org.numenta.sanity.viz_layouts.highlight_rect(ctx,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(x - (0)),cljs.core.cst$kw$y,((y - (1)) - scroll_off),cljs.core.cst$kw$w,(cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(bb) + (0)),cljs.core.cst$kw$h,((cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(bb) + (2)) + scroll_off)], null),color);
});
/**
 * Draw highlight bar horizontally to left axis from element.
 */
org.numenta.sanity.viz_layouts.highlight_element = (function org$numenta$sanity$viz_layouts$highlight_element(lay,ctx,dt,id,label,color){
var vec__47175 = org.numenta.sanity.viz_layouts.origin_px_topleft(lay,dt);
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47175,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47175,(1),null);
var vec__47176 = org.numenta.sanity.viz_layouts.local_px_topleft(lay,id);
var lx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47176,(0),null);
var ly = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47176,(1),null);
var bb = org.numenta.sanity.viz_layouts.layout_bounds(lay);
var vec__47177 = org.numenta.sanity.viz_layouts.element_size_px(lay);
var element_w = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47177,(0),null);
var element_h = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47177,(1),null);
var rect = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(bb) - (1)),cljs.core.cst$kw$y,((y + ly) - (1)),cljs.core.cst$kw$w,((((x - cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(bb)) + lx) + element_w) + (2)),cljs.core.cst$kw$h,(element_h + (2))], null);
org.numenta.sanity.viz_layouts.highlight_rect(ctx,rect,color);

if(cljs.core.truth_(label)){
monet.canvas.save(ctx);

monet.canvas.text_align(ctx,cljs.core.cst$kw$right);

monet.canvas.text_baseline(ctx,cljs.core.cst$kw$middle);

monet.canvas.fill_style(ctx,"black");

monet.canvas.text(ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,(cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(rect) - (1)),cljs.core.cst$kw$y,(cljs.core.cst$kw$y.cljs$core$IFn$_invoke$arity$1(rect) + (element_h / (2))),cljs.core.cst$kw$text,label], null));

return monet.canvas.restore(ctx);
} else {
return null;
}
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.numenta.sanity.viz_layouts.PArrayLayout}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {org.numenta.sanity.viz_layouts.PBox}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PTopological}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.numenta.sanity.viz_layouts.Grid1dLayout = (function (topo,scroll_top,dt_offset,draw_steps,element_w,element_h,shrink,left_px,top_px,max_bottom_px,circles_QMARK_,__meta,__extmap,__hash){
this.topo = topo;
this.scroll_top = scroll_top;
this.dt_offset = dt_offset;
this.draw_steps = draw_steps;
this.element_w = element_w;
this.element_h = element_h;
this.shrink = shrink;
this.left_px = left_px;
this.top_px = top_px;
this.max_bottom_px = max_bottom_px;
this.circles_QMARK_ = circles_QMARK_;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k47179,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__47181 = (((k47179 instanceof cljs.core.Keyword))?k47179.fqn:null);
switch (G__47181) {
case "scroll-top":
return self__.scroll_top;

break;
case "topo":
return self__.topo;

break;
case "element-h":
return self__.element_h;

break;
case "dt-offset":
return self__.dt_offset;

break;
case "shrink":
return self__.shrink;

break;
case "draw-steps":
return self__.draw_steps;

break;
case "max-bottom-px":
return self__.max_bottom_px;

break;
case "top-px":
return self__.top_px;

break;
case "left-px":
return self__.left_px;

break;
case "circles?":
return self__.circles_QMARK_;

break;
case "element-w":
return self__.element_w;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k47179,else__6770__auto__);

}
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.topo;
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.viz-layouts.Grid1dLayout{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 11, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$scroll_DASH_top,self__.scroll_top],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$dt_DASH_offset,self__.dt_offset],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$draw_DASH_steps,self__.draw_steps],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_w,self__.element_w],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_h,self__.element_h],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$shrink,self__.shrink],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$left_DASH_px,self__.left_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$top_DASH_px,self__.top_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$max_DASH_bottom_DASH_px,self__.max_bottom_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$circles_QMARK_,self__.circles_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__47178){
var self__ = this;
var G__47178__$1 = this;
return (new cljs.core.RecordIter((0),G__47178__$1,11,new cljs.core.PersistentVector(null, 11, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$topo,cljs.core.cst$kw$scroll_DASH_top,cljs.core.cst$kw$dt_DASH_offset,cljs.core.cst$kw$draw_DASH_steps,cljs.core.cst$kw$element_DASH_w,cljs.core.cst$kw$element_DASH_h,cljs.core.cst$kw$shrink,cljs.core.cst$kw$left_DASH_px,cljs.core.cst$kw$top_DASH_px,cljs.core.cst$kw$max_DASH_bottom_DASH_px,cljs.core.cst$kw$circles_QMARK_], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (11 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ = true;

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$local_dt_bounds$arity$2 = (function (this$,dt){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(org.numenta.sanity.viz_layouts.layout_bounds(this$__$1),cljs.core.cst$kw$x,(0),cljs.core.array_seq([cljs.core.cst$kw$y,(0),cljs.core.cst$kw$w,self__.element_w], 0));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen_count$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
var G__47182 = org.nfrac.comportex.protocols.size(self__.topo);
if(cljs.core.truth_(self__.max_bottom_px)){
var x__6491__auto__ = G__47182;
var y__6492__auto__ = cljs.core.quot((self__.max_bottom_px - self__.top_px),self__.element_h);
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
} else {
return G__47182;
}
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$element_size_px$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [self__.element_w,self__.element_h], null);
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$draw_element$arity$3 = (function (this$,ctx,id){
var self__ = this;
var this$__$1 = this;
var vec__47183 = org.numenta.sanity.viz_layouts.local_px_topleft(this$__$1,id);
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47183,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47183,(1),null);
if(cljs.core.truth_(self__.circles_QMARK_)){
return org.numenta.sanity.viz_layouts.circle_from_bounds(ctx,x,y,(self__.element_w * self__.shrink));
} else {
return ctx.rect(x,y,(self__.element_w * self__.shrink),(self__.element_h * self__.shrink));
}
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$id_onscreen_QMARK_$arity$2 = (function (this$,id){
var self__ = this;
var this$__$1 = this;
var n = org.numenta.sanity.viz_layouts.ids_onscreen_count(this$__$1);
var n0 = self__.scroll_top;
return ((n0 <= id)) && ((id < (n0 + n)));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_count$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.size(self__.topo);
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var n0 = self__.scroll_top;
return cljs.core.range.cljs$core$IFn$_invoke$arity$2(n0,(n0 + org.numenta.sanity.viz_layouts.ids_onscreen_count(this$__$1)));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$scroll_position$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.scroll_top;
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$origin_px_topleft$arity$2 = (function (_,dt){
var self__ = this;
var ___$1 = this;
var right = (self__.left_px + (self__.draw_steps * self__.element_w));
var off_x_px = (((dt + (1)) - self__.dt_offset) * self__.element_w);
var x_px = (right - off_x_px);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_px,self__.top_px], null);
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$scroll$arity$2 = (function (this$,down_QMARK_){
var self__ = this;
var this$__$1 = this;
var page_n = org.numenta.sanity.viz_layouts.ids_onscreen_count(this$__$1);
var n_ids = org.nfrac.comportex.protocols.size(self__.topo);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$scroll_DASH_top,(cljs.core.truth_(down_QMARK_)?(((self__.scroll_top < (n_ids - page_n)))?(self__.scroll_top + page_n):self__.scroll_top):(function (){var x__6484__auto__ = (0);
var y__6485__auto__ = (self__.scroll_top - page_n);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})()));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$local_px_topleft$arity$2 = (function (_,id){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),((id - self__.scroll_top) * self__.element_h)], null);
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$clicked_id$arity$3 = (function (this$,x,y){
var self__ = this;
var this$__$1 = this;
var right = (self__.left_px + (self__.draw_steps * self__.element_w));
var dt_STAR_ = (function (){var G__47184 = ((right - x) / self__.element_w);
return Math.floor(G__47184);
})();
var id_STAR_ = (function (){var G__47185 = ((y - self__.top_px) / self__.element_h);
return Math.floor(G__47185);
})();
var id = (id_STAR_ + self__.scroll_top);
var dt = (dt_STAR_ + self__.dt_offset);
if((((0) <= dt_STAR_)) && ((dt_STAR_ <= self__.draw_steps))){
if(cljs.core.truth_(org.numenta.sanity.viz_layouts.id_onscreen_QMARK_(this$__$1,id))){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [dt,id], null);
} else {
if((y <= self__.top_px)){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [dt,null], null);
} else {
return null;
}
}
} else {
return null;
}
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 11, [cljs.core.cst$kw$scroll_DASH_top,null,cljs.core.cst$kw$topo,null,cljs.core.cst$kw$element_DASH_h,null,cljs.core.cst$kw$dt_DASH_offset,null,cljs.core.cst$kw$shrink,null,cljs.core.cst$kw$draw_DASH_steps,null,cljs.core.cst$kw$max_DASH_bottom_DASH_px,null,cljs.core.cst$kw$top_DASH_px,null,cljs.core.cst$kw$left_DASH_px,null,cljs.core.cst$kw$circles_QMARK_,null,cljs.core.cst$kw$element_DASH_w,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__47178){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__47186 = cljs.core.keyword_identical_QMARK_;
var expr__47187 = k__6775__auto__;
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$topo,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$topo,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(G__47178,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$scroll_DASH_top,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$scroll_DASH_top,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,G__47178,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$dt_DASH_offset,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$dt_DASH_offset,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,G__47178,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$draw_DASH_steps,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$draw_DASH_steps,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,G__47178,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$element_DASH_w,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$element_DASH_w,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,G__47178,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$element_DASH_h,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$element_DASH_h,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,G__47178,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$shrink,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$shrink,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,G__47178,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$left_DASH_px,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$left_DASH_px,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,G__47178,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$top_DASH_px,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$top_DASH_px,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,G__47178,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$max_DASH_bottom_DASH_px,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$max_DASH_bottom_DASH_px,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,G__47178,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47186.cljs$core$IFn$_invoke$arity$2 ? pred__47186.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$circles_QMARK_,expr__47187) : pred__47186.call(null,cljs.core.cst$kw$circles_QMARK_,expr__47187)))){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,G__47178,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__47178),null));
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
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PBox$ = true;

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.org$numenta$sanity$viz_layouts$PBox$layout_bounds$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,self__.left_px,cljs.core.cst$kw$y,self__.top_px,cljs.core.cst$kw$w,(self__.draw_steps * self__.element_w),cljs.core.cst$kw$h,(function (){var G__47189 = (org.nfrac.comportex.protocols.size(self__.topo) * self__.element_h);
if(cljs.core.truth_(self__.max_bottom_px)){
var x__6491__auto__ = G__47189;
var y__6492__auto__ = (self__.max_bottom_px - self__.top_px);
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
} else {
return G__47189;
}
})()], null);
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 11, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$scroll_DASH_top,self__.scroll_top],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$dt_DASH_offset,self__.dt_offset],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$draw_DASH_steps,self__.draw_steps],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_w,self__.element_w],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_h,self__.element_h],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$shrink,self__.shrink],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$left_DASH_px,self__.left_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$top_DASH_px,self__.top_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$max_DASH_bottom_DASH_px,self__.max_bottom_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$circles_QMARK_,self__.circles_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__47178){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(self__.topo,self__.scroll_top,self__.dt_offset,self__.draw_steps,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,G__47178,self__.__extmap,self__.__hash));
});

org.numenta.sanity.viz_layouts.Grid1dLayout.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.viz_layouts.Grid1dLayout.getBasis = (function (){
return new cljs.core.PersistentVector(null, 11, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$topo,cljs.core.cst$sym$scroll_DASH_top,cljs.core.cst$sym$dt_DASH_offset,cljs.core.cst$sym$draw_DASH_steps,cljs.core.cst$sym$element_DASH_w,cljs.core.cst$sym$element_DASH_h,cljs.core.cst$sym$shrink,cljs.core.cst$sym$left_DASH_px,cljs.core.cst$sym$top_DASH_px,cljs.core.cst$sym$max_DASH_bottom_DASH_px,cljs.core.cst$sym$circles_QMARK_], null);
});

org.numenta.sanity.viz_layouts.Grid1dLayout.cljs$lang$type = true;

org.numenta.sanity.viz_layouts.Grid1dLayout.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.viz-layouts/Grid1dLayout");
});

org.numenta.sanity.viz_layouts.Grid1dLayout.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.viz-layouts/Grid1dLayout");
});

org.numenta.sanity.viz_layouts.__GT_Grid1dLayout = (function org$numenta$sanity$viz_layouts$__GT_Grid1dLayout(topo,scroll_top,dt_offset,draw_steps,element_w,element_h,shrink,left_px,top_px,max_bottom_px,circles_QMARK_){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(topo,scroll_top,dt_offset,draw_steps,element_w,element_h,shrink,left_px,top_px,max_bottom_px,circles_QMARK_,null,null,null));
});

org.numenta.sanity.viz_layouts.map__GT_Grid1dLayout = (function org$numenta$sanity$viz_layouts$map__GT_Grid1dLayout(G__47180){
return (new org.numenta.sanity.viz_layouts.Grid1dLayout(cljs.core.cst$kw$topo.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$scroll_DASH_top.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$dt_DASH_offset.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$draw_DASH_steps.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$element_DASH_w.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$element_DASH_h.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$shrink.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$left_DASH_px.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$top_DASH_px.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$max_DASH_bottom_DASH_px.cljs$core$IFn$_invoke$arity$1(G__47180),cljs.core.cst$kw$circles_QMARK_.cljs$core$IFn$_invoke$arity$1(G__47180),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__47180,cljs.core.cst$kw$topo,cljs.core.array_seq([cljs.core.cst$kw$scroll_DASH_top,cljs.core.cst$kw$dt_DASH_offset,cljs.core.cst$kw$draw_DASH_steps,cljs.core.cst$kw$element_DASH_w,cljs.core.cst$kw$element_DASH_h,cljs.core.cst$kw$shrink,cljs.core.cst$kw$left_DASH_px,cljs.core.cst$kw$top_DASH_px,cljs.core.cst$kw$max_DASH_bottom_DASH_px,cljs.core.cst$kw$circles_QMARK_], 0)),null));
});

org.numenta.sanity.viz_layouts.grid_1d_layout = (function org$numenta$sanity$viz_layouts$grid_1d_layout(topo,top,left,opts,inbits_QMARK_){
var map__47193 = opts;
var map__47193__$1 = ((((!((map__47193 == null)))?((((map__47193.cljs$lang$protocol_mask$partition0$ & (64))) || (map__47193.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__47193):map__47193);
var draw_steps = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47193__$1,cljs.core.cst$kw$draw_DASH_steps);
var max_height_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47193__$1,cljs.core.cst$kw$max_DASH_height_DASH_px);
var col_d_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47193__$1,cljs.core.cst$kw$col_DASH_d_DASH_px);
var col_shrink = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47193__$1,cljs.core.cst$kw$col_DASH_shrink);
var bit_w_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47193__$1,cljs.core.cst$kw$bit_DASH_w_DASH_px);
var bit_h_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47193__$1,cljs.core.cst$kw$bit_DASH_h_DASH_px);
var bit_shrink = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47193__$1,cljs.core.cst$kw$bit_DASH_shrink);
return org.numenta.sanity.viz_layouts.map__GT_Grid1dLayout(cljs.core.PersistentHashMap.fromArrays([cljs.core.cst$kw$scroll_DASH_top,cljs.core.cst$kw$topo,cljs.core.cst$kw$element_DASH_h,cljs.core.cst$kw$dt_DASH_offset,cljs.core.cst$kw$shrink,cljs.core.cst$kw$draw_DASH_steps,cljs.core.cst$kw$max_DASH_bottom_DASH_px,cljs.core.cst$kw$top_DASH_px,cljs.core.cst$kw$left_DASH_px,cljs.core.cst$kw$circles_QMARK_,cljs.core.cst$kw$element_DASH_w],[(0),topo,(cljs.core.truth_(inbits_QMARK_)?bit_h_px:col_d_px),(0),(cljs.core.truth_(inbits_QMARK_)?bit_shrink:col_shrink),draw_steps,(cljs.core.truth_(max_height_px)?(max_height_px - org.numenta.sanity.viz_layouts.extra_px_for_highlight):null),top,left,(cljs.core.truth_(inbits_QMARK_)?false:true),(cljs.core.truth_(inbits_QMARK_)?bit_w_px:col_d_px)]));
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.numenta.sanity.viz_layouts.PArrayLayout}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {org.numenta.sanity.viz_layouts.PBox}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PTopological}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.numenta.sanity.viz_layouts.Grid2dLayout = (function (n_elements,topo,scroll_top,element_w,element_h,shrink,left_px,top_px,max_bottom_px,circles_QMARK_,__meta,__extmap,__hash){
this.n_elements = n_elements;
this.topo = topo;
this.scroll_top = scroll_top;
this.element_w = element_w;
this.element_h = element_h;
this.shrink = shrink;
this.left_px = left_px;
this.top_px = top_px;
this.max_bottom_px = max_bottom_px;
this.circles_QMARK_ = circles_QMARK_;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k47196,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__47198 = (((k47196 instanceof cljs.core.Keyword))?k47196.fqn:null);
switch (G__47198) {
case "scroll-top":
return self__.scroll_top;

break;
case "topo":
return self__.topo;

break;
case "element-h":
return self__.element_h;

break;
case "shrink":
return self__.shrink;

break;
case "max-bottom-px":
return self__.max_bottom_px;

break;
case "n-elements":
return self__.n_elements;

break;
case "top-px":
return self__.top_px;

break;
case "left-px":
return self__.left_px;

break;
case "circles?":
return self__.circles_QMARK_;

break;
case "element-w":
return self__.element_w;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k47196,else__6770__auto__);

}
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.topo;
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.viz-layouts.Grid2dLayout{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 10, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$n_DASH_elements,self__.n_elements],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$scroll_DASH_top,self__.scroll_top],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_w,self__.element_w],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_h,self__.element_h],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$shrink,self__.shrink],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$left_DASH_px,self__.left_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$top_DASH_px,self__.top_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$max_DASH_bottom_DASH_px,self__.max_bottom_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$circles_QMARK_,self__.circles_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__47195){
var self__ = this;
var G__47195__$1 = this;
return (new cljs.core.RecordIter((0),G__47195__$1,10,new cljs.core.PersistentVector(null, 10, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$n_DASH_elements,cljs.core.cst$kw$topo,cljs.core.cst$kw$scroll_DASH_top,cljs.core.cst$kw$element_DASH_w,cljs.core.cst$kw$element_DASH_h,cljs.core.cst$kw$shrink,cljs.core.cst$kw$left_DASH_px,cljs.core.cst$kw$top_DASH_px,cljs.core.cst$kw$max_DASH_bottom_DASH_px,cljs.core.cst$kw$circles_QMARK_], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (10 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ = true;

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$local_dt_bounds$arity$2 = (function (this$,dt){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(org.numenta.sanity.viz_layouts.layout_bounds(this$__$1),cljs.core.cst$kw$x,(0),cljs.core.array_seq([cljs.core.cst$kw$y,(0)], 0));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen_count$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
var vec__47199 = org.nfrac.comportex.protocols.dimensions(self__.topo);
var w = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47199,(0),null);
var h = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47199,(1),null);
var x__6491__auto__ = self__.n_elements;
var y__6492__auto__ = (w * (function (){var G__47200 = h;
if(cljs.core.truth_(self__.max_bottom_px)){
var x__6491__auto____$1 = G__47200;
var y__6492__auto__ = cljs.core.quot((self__.max_bottom_px - self__.top_px),self__.element_h);
return ((x__6491__auto____$1 < y__6492__auto__) ? x__6491__auto____$1 : y__6492__auto__);
} else {
return G__47200;
}
})());
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$element_size_px$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [self__.element_w,self__.element_h], null);
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$draw_element$arity$3 = (function (this$,ctx,id){
var self__ = this;
var this$__$1 = this;
var vec__47201 = org.numenta.sanity.viz_layouts.local_px_topleft(this$__$1,id);
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47201,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47201,(1),null);
if(cljs.core.truth_(self__.circles_QMARK_)){
return org.numenta.sanity.viz_layouts.circle_from_bounds(ctx,x,y,(self__.element_w * self__.shrink));
} else {
return ctx.rect(x,y,(self__.element_w * self__.shrink),(self__.element_h * self__.shrink));
}
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$id_onscreen_QMARK_$arity$2 = (function (this$,id){
var self__ = this;
var this$__$1 = this;
var n0 = self__.scroll_top;
return ((n0 <= id)) && ((id < (n0 + org.numenta.sanity.viz_layouts.ids_onscreen_count(this$__$1))));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_count$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.n_elements;
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var n0 = self__.scroll_top;
return cljs.core.range.cljs$core$IFn$_invoke$arity$2(n0,(n0 + org.numenta.sanity.viz_layouts.ids_onscreen_count(this$__$1)));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$scroll_position$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return self__.scroll_top;
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$origin_px_topleft$arity$2 = (function (_,dt){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [self__.left_px,self__.top_px], null);
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$scroll$arity$2 = (function (this$,down_QMARK_){
var self__ = this;
var this$__$1 = this;
var page_n = org.numenta.sanity.viz_layouts.ids_onscreen_count(this$__$1);
var n_ids = org.nfrac.comportex.protocols.size(self__.topo);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$scroll_DASH_top,(cljs.core.truth_(down_QMARK_)?(((self__.scroll_top < (n_ids - page_n)))?(self__.scroll_top + page_n):self__.scroll_top):(function (){var x__6484__auto__ = (0);
var y__6485__auto__ = (self__.scroll_top - page_n);
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})()));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$local_px_topleft$arity$2 = (function (_,id){
var self__ = this;
var ___$1 = this;
var vec__47202 = org.nfrac.comportex.protocols.coordinates_of_index(self__.topo,(id + self__.scroll_top));
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47202,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47202,(1),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(x * self__.element_w),(y * self__.element_h)], null);
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$clicked_id$arity$3 = (function (_,x,y){
var self__ = this;
var ___$1 = this;
var vec__47203 = org.nfrac.comportex.protocols.dimensions(self__.topo);
var w = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47203,(0),null);
var h = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47203,(1),null);
var xi = (function (){var G__47204 = ((x - self__.left_px) / self__.element_w);
return Math.floor(G__47204);
})();
var yi = (function (){var G__47205 = ((y - self__.top_px) / self__.element_h);
return Math.floor(G__47205);
})();
if(((((0) <= xi)) && ((xi <= (w - (1))))) && ((yi <= (h - (1))))){
if((y >= (0))){
var id_STAR_ = org.nfrac.comportex.protocols.index_of_coordinates(self__.topo,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [xi,yi], null));
var id = (id_STAR_ - self__.scroll_top);
if((id < self__.n_elements)){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),id], null);
} else {
return null;
}
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),null], null);
}
} else {
return null;
}
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 10, [cljs.core.cst$kw$scroll_DASH_top,null,cljs.core.cst$kw$topo,null,cljs.core.cst$kw$element_DASH_h,null,cljs.core.cst$kw$shrink,null,cljs.core.cst$kw$max_DASH_bottom_DASH_px,null,cljs.core.cst$kw$n_DASH_elements,null,cljs.core.cst$kw$top_DASH_px,null,cljs.core.cst$kw$left_DASH_px,null,cljs.core.cst$kw$circles_QMARK_,null,cljs.core.cst$kw$element_DASH_w,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__47195){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__47206 = cljs.core.keyword_identical_QMARK_;
var expr__47207 = k__6775__auto__;
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$n_DASH_elements,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$n_DASH_elements,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(G__47195,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$topo,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$topo,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,G__47195,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$scroll_DASH_top,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$scroll_DASH_top,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,G__47195,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$element_DASH_w,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$element_DASH_w,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,G__47195,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$element_DASH_h,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$element_DASH_h,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,G__47195,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$shrink,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$shrink,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,G__47195,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$left_DASH_px,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$left_DASH_px,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,G__47195,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$top_DASH_px,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$top_DASH_px,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,G__47195,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$max_DASH_bottom_DASH_px,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$max_DASH_bottom_DASH_px,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,G__47195,self__.circles_QMARK_,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47206.cljs$core$IFn$_invoke$arity$2 ? pred__47206.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$circles_QMARK_,expr__47207) : pred__47206.call(null,cljs.core.cst$kw$circles_QMARK_,expr__47207)))){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,G__47195,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__47195),null));
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
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PBox$ = true;

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.org$numenta$sanity$viz_layouts$PBox$layout_bounds$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
var vec__47209 = org.nfrac.comportex.protocols.dimensions(self__.topo);
var w = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47209,(0),null);
var h = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47209,(1),null);
return new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,self__.left_px,cljs.core.cst$kw$y,self__.top_px,cljs.core.cst$kw$w,(w * self__.element_w),cljs.core.cst$kw$h,(function (){var G__47210 = (h * self__.element_h);
if(cljs.core.truth_(self__.max_bottom_px)){
var x__6491__auto__ = G__47210;
var y__6492__auto__ = (self__.max_bottom_px - self__.top_px);
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
} else {
return G__47210;
}
})()], null);
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 10, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$n_DASH_elements,self__.n_elements],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$topo,self__.topo],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$scroll_DASH_top,self__.scroll_top],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_w,self__.element_w],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$element_DASH_h,self__.element_h],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$shrink,self__.shrink],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$left_DASH_px,self__.left_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$top_DASH_px,self__.top_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$max_DASH_bottom_DASH_px,self__.max_bottom_px],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$circles_QMARK_,self__.circles_QMARK_],null))], null),self__.__extmap));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__47195){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(self__.n_elements,self__.topo,self__.scroll_top,self__.element_w,self__.element_h,self__.shrink,self__.left_px,self__.top_px,self__.max_bottom_px,self__.circles_QMARK_,G__47195,self__.__extmap,self__.__hash));
});

org.numenta.sanity.viz_layouts.Grid2dLayout.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.viz_layouts.Grid2dLayout.getBasis = (function (){
return new cljs.core.PersistentVector(null, 10, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$n_DASH_elements,cljs.core.cst$sym$topo,cljs.core.cst$sym$scroll_DASH_top,cljs.core.cst$sym$element_DASH_w,cljs.core.cst$sym$element_DASH_h,cljs.core.cst$sym$shrink,cljs.core.cst$sym$left_DASH_px,cljs.core.cst$sym$top_DASH_px,cljs.core.cst$sym$max_DASH_bottom_DASH_px,cljs.core.cst$sym$circles_QMARK_], null);
});

org.numenta.sanity.viz_layouts.Grid2dLayout.cljs$lang$type = true;

org.numenta.sanity.viz_layouts.Grid2dLayout.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.viz-layouts/Grid2dLayout");
});

org.numenta.sanity.viz_layouts.Grid2dLayout.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.viz-layouts/Grid2dLayout");
});

org.numenta.sanity.viz_layouts.__GT_Grid2dLayout = (function org$numenta$sanity$viz_layouts$__GT_Grid2dLayout(n_elements,topo,scroll_top,element_w,element_h,shrink,left_px,top_px,max_bottom_px,circles_QMARK_){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(n_elements,topo,scroll_top,element_w,element_h,shrink,left_px,top_px,max_bottom_px,circles_QMARK_,null,null,null));
});

org.numenta.sanity.viz_layouts.map__GT_Grid2dLayout = (function org$numenta$sanity$viz_layouts$map__GT_Grid2dLayout(G__47197){
return (new org.numenta.sanity.viz_layouts.Grid2dLayout(cljs.core.cst$kw$n_DASH_elements.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$topo.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$scroll_DASH_top.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$element_DASH_w.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$element_DASH_h.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$shrink.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$left_DASH_px.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$top_DASH_px.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$max_DASH_bottom_DASH_px.cljs$core$IFn$_invoke$arity$1(G__47197),cljs.core.cst$kw$circles_QMARK_.cljs$core$IFn$_invoke$arity$1(G__47197),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__47197,cljs.core.cst$kw$n_DASH_elements,cljs.core.array_seq([cljs.core.cst$kw$topo,cljs.core.cst$kw$scroll_DASH_top,cljs.core.cst$kw$element_DASH_w,cljs.core.cst$kw$element_DASH_h,cljs.core.cst$kw$shrink,cljs.core.cst$kw$left_DASH_px,cljs.core.cst$kw$top_DASH_px,cljs.core.cst$kw$max_DASH_bottom_DASH_px,cljs.core.cst$kw$circles_QMARK_], 0)),null));
});

org.numenta.sanity.viz_layouts.grid_2d_layout = (function org$numenta$sanity$viz_layouts$grid_2d_layout(n_elements,topo,top,left,opts,inbits_QMARK_){
var map__47214 = opts;
var map__47214__$1 = ((((!((map__47214 == null)))?((((map__47214.cljs$lang$protocol_mask$partition0$ & (64))) || (map__47214.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__47214):map__47214);
var max_height_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47214__$1,cljs.core.cst$kw$max_DASH_height_DASH_px);
var col_d_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47214__$1,cljs.core.cst$kw$col_DASH_d_DASH_px);
var col_shrink = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47214__$1,cljs.core.cst$kw$col_DASH_shrink);
var bit_w_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47214__$1,cljs.core.cst$kw$bit_DASH_w_DASH_px);
var bit_h_px = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47214__$1,cljs.core.cst$kw$bit_DASH_h_DASH_px);
var bit_shrink = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47214__$1,cljs.core.cst$kw$bit_DASH_shrink);
return org.numenta.sanity.viz_layouts.map__GT_Grid2dLayout(cljs.core.PersistentHashMap.fromArrays([cljs.core.cst$kw$scroll_DASH_top,cljs.core.cst$kw$topo,cljs.core.cst$kw$element_DASH_h,cljs.core.cst$kw$shrink,cljs.core.cst$kw$max_DASH_bottom_DASH_px,cljs.core.cst$kw$n_DASH_elements,cljs.core.cst$kw$top_DASH_px,cljs.core.cst$kw$left_DASH_px,cljs.core.cst$kw$circles_QMARK_,cljs.core.cst$kw$element_DASH_w],[(0),topo,(cljs.core.truth_(inbits_QMARK_)?bit_h_px:col_d_px),(cljs.core.truth_(inbits_QMARK_)?bit_shrink:col_shrink),(cljs.core.truth_(max_height_px)?(max_height_px - org.numenta.sanity.viz_layouts.extra_px_for_highlight):null),n_elements,top,left,(cljs.core.truth_(inbits_QMARK_)?false:true),(cljs.core.truth_(inbits_QMARK_)?bit_w_px:col_d_px)]));
});
org.numenta.sanity.viz_layouts.grid_layout = (function org$numenta$sanity$viz_layouts$grid_layout(dims,top,left,opts,inbits_QMARK_,display_mode){
var n_elements = cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core._STAR_,dims);
var G__47222 = (((display_mode instanceof cljs.core.Keyword))?display_mode.fqn:null);
switch (G__47222) {
case "one-d":
return org.numenta.sanity.viz_layouts.grid_1d_layout(org.nfrac.comportex.topology.one_d_topology(n_elements),top,left,opts,inbits_QMARK_);

break;
case "two-d":
var vec__47223 = (function (){var G__47224 = cljs.core.count(dims);
switch (G__47224) {
case (2):
return dims;

break;
case (1):
var w = (function (){var x__6491__auto__ = (function (){var G__47225 = Math.sqrt(n_elements);
return Math.ceil(G__47225);
})();
var y__6492__auto__ = (20);
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})();
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [w,(function (){var G__47226 = (n_elements / w);
return Math.ceil(G__47226);
})()], null);

break;
case (3):
var vec__47227 = dims;
var w = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47227,(0),null);
var h = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47227,(1),null);
var d = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47227,(2),null);
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [w,(h * d)], null);

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(cljs.core.count(dims))].join('')));

}
})();
var width = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47223,(0),null);
var height = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47223,(1),null);
return org.numenta.sanity.viz_layouts.grid_2d_layout(n_elements,org.nfrac.comportex.topology.two_d_topology(width,height),top,left,opts,inbits_QMARK_);

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(display_mode)].join('')));

}
});

/**
 * @interface
 */
org.numenta.sanity.viz_layouts.POrderable = function(){};

org.numenta.sanity.viz_layouts.reorder = (function org$numenta$sanity$viz_layouts$reorder(this$,ordered_ids){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$POrderable$reorder$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$POrderable$reorder$arity$2(this$,ordered_ids);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.reorder[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,ordered_ids) : m__6809__auto__.call(null,this$,ordered_ids));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.reorder["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,ordered_ids) : m__6809__auto____$1.call(null,this$,ordered_ids));
} else {
throw cljs.core.missing_protocol("POrderable.reorder",this$);
}
}
}
});


/**
 * @interface
 */
org.numenta.sanity.viz_layouts.PTemporalSortable = function(){};

org.numenta.sanity.viz_layouts.sort_by_recent_activity = (function org$numenta$sanity$viz_layouts$sort_by_recent_activity(this$,ids_ts){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PTemporalSortable$sort_by_recent_activity$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$PTemporalSortable$sort_by_recent_activity$arity$2(this$,ids_ts);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.sort_by_recent_activity[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,ids_ts) : m__6809__auto__.call(null,this$,ids_ts));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.sort_by_recent_activity["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,ids_ts) : m__6809__auto____$1.call(null,this$,ids_ts));
} else {
throw cljs.core.missing_protocol("PTemporalSortable.sort-by-recent-activity",this$);
}
}
}
});

org.numenta.sanity.viz_layouts.clear_sort = (function org$numenta$sanity$viz_layouts$clear_sort(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PTemporalSortable$clear_sort$arity$1 == null)))){
return this$.org$numenta$sanity$viz_layouts$PTemporalSortable$clear_sort$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.clear_sort[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.clear_sort["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PTemporalSortable.clear-sort",this$);
}
}
}
});

org.numenta.sanity.viz_layouts.add_facet = (function org$numenta$sanity$viz_layouts$add_facet(this$,ids,label){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PTemporalSortable$add_facet$arity$3 == null)))){
return this$.org$numenta$sanity$viz_layouts$PTemporalSortable$add_facet$arity$3(this$,ids,label);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.add_facet[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,ids,label) : m__6809__auto__.call(null,this$,ids,label));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.add_facet["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,ids,label) : m__6809__auto____$1.call(null,this$,ids,label));
} else {
throw cljs.core.missing_protocol("PTemporalSortable.add-facet",this$);
}
}
}
});

org.numenta.sanity.viz_layouts.clear_facets = (function org$numenta$sanity$viz_layouts$clear_facets(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PTemporalSortable$clear_facets$arity$1 == null)))){
return this$.org$numenta$sanity$viz_layouts$PTemporalSortable$clear_facets$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.clear_facets[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.clear_facets["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PTemporalSortable.clear-facets",this$);
}
}
}
});

org.numenta.sanity.viz_layouts.draw_facets = (function org$numenta$sanity$viz_layouts$draw_facets(this$,ctx){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$viz_layouts$PTemporalSortable$draw_facets$arity$2 == null)))){
return this$.org$numenta$sanity$viz_layouts$PTemporalSortable$draw_facets$arity$2(this$,ctx);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.viz_layouts.draw_facets[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,ctx) : m__6809__auto__.call(null,this$,ctx));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.viz_layouts.draw_facets["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,ctx) : m__6809__auto____$1.call(null,this$,ctx));
} else {
throw cljs.core.missing_protocol("PTemporalSortable.draw-facets",this$);
}
}
}
});


/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {org.numenta.sanity.viz_layouts.PArrayLayout}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {org.numenta.sanity.viz_layouts.PTemporalSortable}
 * @implements {org.numenta.sanity.viz_layouts.PBox}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {org.numenta.sanity.viz_layouts.POrderable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {org.nfrac.comportex.protocols.PTopological}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.numenta.sanity.viz_layouts.OrderableLayout = (function (layout,order,facets,__meta,__extmap,__hash){
this.layout = layout;
this.order = order;
this.facets = facets;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k47232,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__47234 = (((k47232 instanceof cljs.core.Keyword))?k47232.fqn:null);
switch (G__47234) {
case "layout":
return self__.layout;

break;
case "order":
return self__.order;

break;
case "facets":
return self__.facets;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k47232,else__6770__auto__);

}
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$nfrac$comportex$protocols$PTopological$ = true;

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$nfrac$comportex$protocols$PTopological$topology$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.nfrac.comportex.protocols.topology(self__.layout);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.viz-layouts.OrderableLayout{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layout,self__.layout],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$order,self__.order],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$facets,self__.facets],null))], null),self__.__extmap));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__47231){
var self__ = this;
var G__47231__$1 = this;
return (new cljs.core.RecordIter((0),G__47231__$1,3,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$layout,cljs.core.cst$kw$order,cljs.core.cst$kw$facets], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.viz_layouts.OrderableLayout(self__.layout,self__.order,self__.facets,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (3 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ = true;

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$local_dt_bounds$arity$2 = (function (_,dt){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.viz_layouts.local_dt_bounds(self__.layout,dt);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen_count$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.viz_layouts.ids_onscreen_count(self__.layout);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$element_size_px$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.viz_layouts.element_size_px(self__.layout);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$draw_element$arity$3 = (function (this$,ctx,id){
var self__ = this;
var this$__$1 = this;
var idx = (self__.order.cljs$core$IFn$_invoke$arity$1 ? self__.order.cljs$core$IFn$_invoke$arity$1(id) : self__.order.call(null,id));
return org.numenta.sanity.viz_layouts.draw_element(self__.layout,ctx,idx);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$id_onscreen_QMARK_$arity$2 = (function (_,id){
var self__ = this;
var ___$1 = this;
var idx = (self__.order.cljs$core$IFn$_invoke$arity$1 ? self__.order.cljs$core$IFn$_invoke$arity$1(id) : self__.order.call(null,id));
return org.numenta.sanity.viz_layouts.id_onscreen_QMARK_(self__.layout,idx);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_count$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.viz_layouts.ids_count(self__.layout);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$ids_onscreen$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
var n0 = org.numenta.sanity.viz_layouts.scroll_position(self__.layout);
return cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.key,cljs.core.subseq.cljs$core$IFn$_invoke$arity$5(self__.order,cljs.core._GT__EQ_,n0,cljs.core._LT_,(n0 + org.numenta.sanity.viz_layouts.ids_onscreen_count(self__.layout))));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$scroll_position$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.viz_layouts.scroll_position(self__.layout);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$origin_px_topleft$arity$2 = (function (_,dt){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.viz_layouts.origin_px_topleft(self__.layout,dt);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$scroll$arity$2 = (function (this$,down_QMARK_){
var self__ = this;
var this$__$1 = this;
return cljs.core.update.cljs$core$IFn$_invoke$arity$4(this$__$1,cljs.core.cst$kw$layout,org.numenta.sanity.viz_layouts.scroll,down_QMARK_);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$local_px_topleft$arity$2 = (function (_,id){
var self__ = this;
var ___$1 = this;
var idx = (self__.order.cljs$core$IFn$_invoke$arity$1 ? self__.order.cljs$core$IFn$_invoke$arity$1(id) : self__.order.call(null,id));
return org.numenta.sanity.viz_layouts.local_px_topleft(self__.layout,idx);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PArrayLayout$clicked_id$arity$3 = (function (this$,x,y){
var self__ = this;
var this$__$1 = this;
var temp__4657__auto__ = org.numenta.sanity.viz_layouts.clicked_id(self__.layout,x,y);
if(cljs.core.truth_(temp__4657__auto__)){
var vec__47235 = temp__4657__auto__;
var dt = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47235,(0),null);
var idx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47235,(1),null);
if(cljs.core.truth_(idx)){
var id = cljs.core.key(cljs.core.first(cljs.core.subseq.cljs$core$IFn$_invoke$arity$5(self__.order,cljs.core._GT__EQ_,idx,cljs.core._LT__EQ_,idx)));
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [dt,id], null);
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [dt,null], null);
}
} else {
return null;
}
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
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

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
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

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$layout,null,cljs.core.cst$kw$order,null,cljs.core.cst$kw$facets,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.viz_layouts.OrderableLayout(self__.layout,self__.order,self__.facets,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$POrderable$ = true;

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$POrderable$reorder$arity$2 = (function (this$,ordered_ids){
var self__ = this;
var this$__$1 = this;
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.count(ordered_ids),cljs.core.count(self__.order))){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$_EQ_,cljs.core.list(cljs.core.cst$sym$count,cljs.core.cst$sym$ordered_DASH_ids),cljs.core.list(cljs.core.cst$sym$count,cljs.core.cst$sym$order))], 0)))].join('')));
}

return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$order,cljs.core.apply.cljs$core$IFn$_invoke$arity$2(tailrecursion.priority_map.priority_map,cljs.core.interleave.cljs$core$IFn$_invoke$arity$2(ordered_ids,cljs.core.range.cljs$core$IFn$_invoke$arity$0())));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PTemporalSortable$ = true;

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PTemporalSortable$sort_by_recent_activity$arity$2 = (function (this$,ids_ts){
var self__ = this;
var this$__$1 = this;
if(cljs.core.every_QMARK_(cljs.core.set_QMARK_,ids_ts)){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$every_QMARK_,cljs.core.cst$sym$set_QMARK_,cljs.core.cst$sym$ids_DASH_ts)], 0)))].join('')));
}

var ftotal = cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core._PLUS_,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.second,self__.facets));
var faceted = cljs.core.take.cljs$core$IFn$_invoke$arity$2(ftotal,cljs.core.keys(self__.order));
var ord_ids = (function (){var ids_ts__$1 = ids_ts;
var ord = cljs.core.transient$(cljs.core.vec(faceted));
var ord_set = cljs.core.transient$(cljs.core.set(faceted));
while(true){
var temp__4655__auto__ = cljs.core.first(ids_ts__$1);
if(cljs.core.truth_(temp__4655__auto__)){
var ids = temp__4655__auto__;
var new_ids = cljs.core.sort_by.cljs$core$IFn$_invoke$arity$2(((function (ids_ts__$1,ord,ord_set,ids,temp__4655__auto__,ftotal,faceted,this$__$1){
return (function (id){
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (ids_ts__$1,ord,ord_set,ids,temp__4655__auto__,ftotal,faceted,this$__$1){
return (function (p1__47230_SHARP_){
return cljs.core.boolean$((p1__47230_SHARP_.cljs$core$IFn$_invoke$arity$1 ? p1__47230_SHARP_.cljs$core$IFn$_invoke$arity$1(id) : p1__47230_SHARP_.call(null,id)));
});})(ids_ts__$1,ord,ord_set,ids,temp__4655__auto__,ftotal,faceted,this$__$1))
,ids_ts__$1);
});})(ids_ts__$1,ord,ord_set,ids,temp__4655__auto__,ftotal,faceted,this$__$1))
,cljs.core.remove.cljs$core$IFn$_invoke$arity$2(ord_set,ids));
var G__47244 = cljs.core.next(ids_ts__$1);
var G__47245 = cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core.conj_BANG_,ord,new_ids);
var G__47246 = cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core.conj_BANG_,ord_set,new_ids);
ids_ts__$1 = G__47244;
ord = G__47245;
ord_set = G__47246;
continue;
} else {
return cljs.core.persistent_BANG_(cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core.conj_BANG_,ord,cljs.core.remove.cljs$core$IFn$_invoke$arity$2(ord_set,cljs.core.range.cljs$core$IFn$_invoke$arity$1(cljs.core.count(self__.order)))));
}
break;
}
})();
return org.numenta.sanity.viz_layouts.reorder(this$__$1,ord_ids);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PTemporalSortable$clear_sort$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
var ftotal = cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core._PLUS_,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.second,self__.facets));
var faceted = cljs.core.take.cljs$core$IFn$_invoke$arity$2(ftotal,cljs.core.keys(self__.order));
var ord_ids = cljs.core.concat.cljs$core$IFn$_invoke$arity$2(faceted,cljs.core.remove.cljs$core$IFn$_invoke$arity$2(cljs.core.set(faceted),cljs.core.range.cljs$core$IFn$_invoke$arity$1(cljs.core.count(self__.order))));
return org.numenta.sanity.viz_layouts.reorder(this$__$1,ord_ids);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PTemporalSortable$add_facet$arity$3 = (function (this$,ids,label){
var self__ = this;
var this$__$1 = this;
var ftotal = cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core._PLUS_,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.second,self__.facets));
var old_faceted = cljs.core.take.cljs$core$IFn$_invoke$arity$2(ftotal,cljs.core.keys(self__.order));
var new_faceted = cljs.core.distinct.cljs$core$IFn$_invoke$arity$1(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(old_faceted,ids));
var new_length = (cljs.core.count(new_faceted) - cljs.core.count(old_faceted));
if((new_length === (0))){
return this$__$1;
} else {
var ord_ids = cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new_faceted,cljs.core.remove.cljs$core$IFn$_invoke$arity$2(cljs.core.set(ids),cljs.core.drop.cljs$core$IFn$_invoke$arity$2(ftotal,cljs.core.keys(self__.order))));
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.viz_layouts.reorder(this$__$1,ord_ids),cljs.core.cst$kw$facets,cljs.core.conj.cljs$core$IFn$_invoke$arity$2(self__.facets,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [label,new_length], null)));
}
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PTemporalSortable$clear_facets$arity$1 = (function (this$){
var self__ = this;
var this$__$1 = this;
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(this$__$1,cljs.core.cst$kw$facets,cljs.core.PersistentVector.EMPTY);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PTemporalSortable$draw_facets$arity$2 = (function (this$,ctx){
var self__ = this;
var this$__$1 = this;
if(cljs.core.seq(self__.facets)){
var bb = org.numenta.sanity.viz_layouts.layout_bounds(this$__$1);
var vec__47236 = org.numenta.sanity.viz_layouts.origin_px_topleft(this$__$1,(0));
var x = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47236,(0),null);
var y = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47236,(1),null);
monet.canvas.stroke_style(ctx,"black");

monet.canvas.fill_style(ctx,"black");

monet.canvas.text_baseline(ctx,cljs.core.cst$kw$bottom);

return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (bb,vec__47236,x,y,this$__$1){
return (function (offset,p__47237){
var vec__47238 = p__47237;
var label = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47238,(0),null);
var length = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47238,(1),null);
var idx = (offset + length);
var vec__47239 = org.numenta.sanity.viz_layouts.local_px_topleft(self__.layout,idx);
var lx = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47239,(0),null);
var ly = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47239,(1),null);
var y_px = (y + ly);
monet.canvas.begin_path(ctx);

monet.canvas.move_to(ctx,cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(bb),y_px);

monet.canvas.line_to(ctx,((cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(bb) + cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(bb)) + (16)),y_px);

monet.canvas.stroke(ctx);

monet.canvas.text(ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,((cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(bb) + cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(bb)) + (3)),cljs.core.cst$kw$y,y_px,cljs.core.cst$kw$text,label], null));

return (offset + length);
});})(bb,vec__47236,x,y,this$__$1))
,(0),self__.facets);
} else {
return null;
}
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__47231){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__47240 = cljs.core.keyword_identical_QMARK_;
var expr__47241 = k__6775__auto__;
if(cljs.core.truth_((pred__47240.cljs$core$IFn$_invoke$arity$2 ? pred__47240.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$layout,expr__47241) : pred__47240.call(null,cljs.core.cst$kw$layout,expr__47241)))){
return (new org.numenta.sanity.viz_layouts.OrderableLayout(G__47231,self__.order,self__.facets,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47240.cljs$core$IFn$_invoke$arity$2 ? pred__47240.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$order,expr__47241) : pred__47240.call(null,cljs.core.cst$kw$order,expr__47241)))){
return (new org.numenta.sanity.viz_layouts.OrderableLayout(self__.layout,G__47231,self__.facets,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__47240.cljs$core$IFn$_invoke$arity$2 ? pred__47240.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$facets,expr__47241) : pred__47240.call(null,cljs.core.cst$kw$facets,expr__47241)))){
return (new org.numenta.sanity.viz_layouts.OrderableLayout(self__.layout,self__.order,G__47231,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.viz_layouts.OrderableLayout(self__.layout,self__.order,self__.facets,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__47231),null));
}
}
}
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PBox$ = true;

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.org$numenta$sanity$viz_layouts$PBox$layout_bounds$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.viz_layouts.layout_bounds(self__.layout);
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$layout,self__.layout],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$order,self__.order],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$facets,self__.facets],null))], null),self__.__extmap));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__47231){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.viz_layouts.OrderableLayout(self__.layout,self__.order,self__.facets,G__47231,self__.__extmap,self__.__hash));
});

org.numenta.sanity.viz_layouts.OrderableLayout.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.viz_layouts.OrderableLayout.getBasis = (function (){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$layout,cljs.core.cst$sym$order,cljs.core.cst$sym$facets], null);
});

org.numenta.sanity.viz_layouts.OrderableLayout.cljs$lang$type = true;

org.numenta.sanity.viz_layouts.OrderableLayout.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.viz-layouts/OrderableLayout");
});

org.numenta.sanity.viz_layouts.OrderableLayout.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.viz-layouts/OrderableLayout");
});

org.numenta.sanity.viz_layouts.__GT_OrderableLayout = (function org$numenta$sanity$viz_layouts$__GT_OrderableLayout(layout,order,facets){
return (new org.numenta.sanity.viz_layouts.OrderableLayout(layout,order,facets,null,null,null));
});

org.numenta.sanity.viz_layouts.map__GT_OrderableLayout = (function org$numenta$sanity$viz_layouts$map__GT_OrderableLayout(G__47233){
return (new org.numenta.sanity.viz_layouts.OrderableLayout(cljs.core.cst$kw$layout.cljs$core$IFn$_invoke$arity$1(G__47233),cljs.core.cst$kw$order.cljs$core$IFn$_invoke$arity$1(G__47233),cljs.core.cst$kw$facets.cljs$core$IFn$_invoke$arity$1(G__47233),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__47233,cljs.core.cst$kw$layout,cljs.core.array_seq([cljs.core.cst$kw$order,cljs.core.cst$kw$facets], 0)),null));
});

org.numenta.sanity.viz_layouts.orderable_layout = (function org$numenta$sanity$viz_layouts$orderable_layout(lay,n_ids){
var order = cljs.core.apply.cljs$core$IFn$_invoke$arity$2(tailrecursion.priority_map.priority_map,cljs.core.interleave.cljs$core$IFn$_invoke$arity$2(cljs.core.range.cljs$core$IFn$_invoke$arity$1(n_ids),cljs.core.range.cljs$core$IFn$_invoke$arity$0()));
return org.numenta.sanity.viz_layouts.map__GT_OrderableLayout(new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$layout,lay,cljs.core.cst$kw$order,order,cljs.core.cst$kw$facets,cljs.core.PersistentVector.EMPTY], null));
});
