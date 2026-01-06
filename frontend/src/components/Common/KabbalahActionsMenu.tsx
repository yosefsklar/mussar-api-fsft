import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import type { KabbalahRead } from "@/client"
import DeleteKabbalah from "../Kabbalot/DeleteKabbalah"
import EditKabbalah from "../Kabbalot/EditKabbalah"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

interface KabbalahActionsMenuProps {
  kabbalah: KabbalahRead
}

export const KabbalahActionsMenu = ({ kabbalah }: KabbalahActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditKabbalah kabbalah={kabbalah} />
        <DeleteKabbalah id={kabbalah.id} />
      </MenuContent>
    </MenuRoot>
  )
}
