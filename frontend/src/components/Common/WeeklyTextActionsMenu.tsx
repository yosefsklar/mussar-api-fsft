import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import type { WeeklyTextRead } from "@/client"
import DeleteWeeklyText from "../WeeklyTexts/DeleteWeeklyText"
import EditWeeklyText from "../WeeklyTexts/EditWeeklyText"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

interface WeeklyTextActionsMenuProps {
  weeklyText: WeeklyTextRead
}

export const WeeklyTextActionsMenu = ({ weeklyText }: WeeklyTextActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditWeeklyText weeklyText={weeklyText} />
        <DeleteWeeklyText id={weeklyText.id} />
      </MenuContent>
    </MenuRoot>
  )
}
