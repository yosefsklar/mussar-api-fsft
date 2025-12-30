import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import type { ReminderPhraseRead } from "@/client"
import DeleteReminderPhrase from "../ReminderPhrases/DeleteReminderPhrase"
import EditReminderPhrase from "../ReminderPhrases/EditReminderPhrase"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

interface ReminderPhraseActionsMenuProps {
  reminderPhrase: ReminderPhraseRead
}

export const ReminderPhraseActionsMenu = ({ reminderPhrase }: ReminderPhraseActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditReminderPhrase reminderPhrase={reminderPhrase} />
        <DeleteReminderPhrase id={reminderPhrase.id} />
      </MenuContent>
    </MenuRoot>
  )
}
