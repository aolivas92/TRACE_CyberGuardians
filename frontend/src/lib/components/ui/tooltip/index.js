import { Tooltip as TooltipPrimitive } from "bits-ui";
import Content from "./tooltip-content.svelte";

const Root = TooltipPrimitive.Root;
const Trigger = TooltipPrimitive.Trigger;
const Provider = TooltipPrimitive.Provider;

export {
	Root,
	Trigger,
	Content,
<<<<<<< HEAD
	Provider as TooltipProvider,
	//
	Root as Tooltip,
	Trigger as TooltipTrigger,
	Content as TooltipContent
=======
	Provider,
	//
	Root as Tooltip,
	Content as TooltipContent,
	Trigger as TooltipTrigger,
	Provider as TooltipProvider,
>>>>>>> dc30d3d4b00bae6865b3c17b35bf8fed636f92d8
};
