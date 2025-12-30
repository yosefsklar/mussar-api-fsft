import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import type { MiddahRead } from "@/client"
import DeleteMiddah from "../Middot/DeleteMiddah"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

interface MiddahActionsMenuProps {
  middah: MiddahRead
}

export const MiddahActionsMenu = ({ middah }: MiddahActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <DeleteMiddah nameTransliterated={middah.name_transliterated} />
      </MenuContent>
    </MenuRoot>
  )
}
