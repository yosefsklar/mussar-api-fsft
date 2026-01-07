import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import type { DailyTextRead } from "@/client"
import DeleteDailyText from "../DailyTexts/DeleteDailyText"
import EditDailyText from "../DailyTexts/EditDailyText"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

interface DailyTextActionsMenuProps {
  dailyText: DailyTextRead
}

export const DailyTextActionsMenu = ({ dailyText }: DailyTextActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditDailyText dailyText={dailyText} />
        <DeleteDailyText id={dailyText.id} />
      </MenuContent>
    </MenuRoot>
  )
}
