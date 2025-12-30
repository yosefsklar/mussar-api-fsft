import type { CollectionItem } from "@chakra-ui/react"
import { Select as ChakraSelect } from "@chakra-ui/react"
import * as React from "react"

export interface SelectTriggerProps extends ChakraSelect.ControlProps {
  clearable?: boolean
}

export const SelectTrigger = React.forwardRef<
  HTMLButtonElement,
  SelectTriggerProps
>(function SelectTrigger(props, ref) {
  const { children, clearable, ...rest } = props
  return (
    <ChakraSelect.Control {...rest}>
      <ChakraSelect.Trigger ref={ref}>{children}</ChakraSelect.Trigger>
      <ChakraSelect.IndicatorGroup>
        {clearable && <ChakraSelect.ClearTrigger />}
        <ChakraSelect.Indicator />
      </ChakraSelect.IndicatorGroup>
    </ChakraSelect.Control>
  )
})

export const SelectContent = React.forwardRef<
  HTMLDivElement,
  ChakraSelect.ContentProps
>(function SelectContent(props, ref) {
  return (
    <ChakraSelect.Positioner>
      <ChakraSelect.Content ref={ref} {...props} />
    </ChakraSelect.Positioner>
  )
})

export const SelectItem = React.forwardRef<
  HTMLDivElement,
  ChakraSelect.ItemProps
>(function SelectItem(props, ref) {
  const { item, children, ...rest } = props
  return (
    <ChakraSelect.Item key={item} item={item} ref={ref} {...rest}>
      {children}
      <ChakraSelect.ItemIndicator />
    </ChakraSelect.Item>
  )
})

export const SelectValueText = React.forwardRef<
  HTMLSpanElement,
  ChakraSelect.ValueTextProps
>(function SelectValueText(props, ref) {
  return <ChakraSelect.ValueText ref={ref} {...props} />
})

export const SelectRoot = React.forwardRef<
  HTMLDivElement,
  ChakraSelect.RootProps<CollectionItem>
>(function SelectRoot(props, ref) {
  return (
    <ChakraSelect.Root ref={ref} {...props} positioning={{ sameWidth: true }}>
      {props.children}
    </ChakraSelect.Root>
  )
})
