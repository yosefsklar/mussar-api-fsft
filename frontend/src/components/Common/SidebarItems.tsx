import { Box, Flex, Icon, Text } from "@chakra-ui/react"
import { useQueryClient } from "@tanstack/react-query"
import { Link as RouterLink } from "@tanstack/react-router"

import { FiBriefcase, FiHome, FiSettings, FiUsers } from "react-icons/fi"
import { IoFlameOutline } from "react-icons/io5"
import { LuSpeech } from "react-icons/lu"
import type { IconType } from "react-icons/lib"

import type { UserPublic } from "@/client"

const items = [
  { icon: FiHome, title: "Dashboard", path: "/" },
  { icon: FiBriefcase, title: "Items", path: "/items" },
  { icon: IoFlameOutline, title: "Middot", path: "/middot" },
  { icon: LuSpeech, title: "Reminder Phrases", path: "/reminder-phrases" },
  { icon: FiSettings, title: "User Settings", path: "/settings" },
]

interface SidebarItemsProps {
  onClose?: () => void
}

interface Item {
  icon: IconType
  title: string
  path: string
}

const SidebarItems = ({ onClose }: SidebarItemsProps) => {
  const queryClient = useQueryClient()
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])

  const finalItems: Item[] = currentUser?.is_superuser
    ? [...items, { icon: FiUsers, title: "Admin", path: "/admin" }]
    : items

  const listItems = finalItems.map(({ icon, title, path }) => (
    <RouterLink key={title} to={path} onClick={onClose}>
      {({ isActive }) => (
        <Flex
          gap={4}
          px={4}
          py={2}
          bg={isActive ? "gray.subtle" : "transparent"}
          color={isActive ? "ui.sidebarRed" : "inherit"}
          _hover={{
            background: isActive ? "gray.subtle" : "ui.sidebarRed",
            color: isActive ? "ui.sidebarRed" : "white",
            textDecoration: "none",
          }}
          alignItems="center"
          fontSize="sm"
        >
          <Icon as={icon} alignSelf="center" />
          <Text ml={2}>{title}</Text>
        </Flex>
      )}
    </RouterLink>
  ))

  return (
    <>
      <Text fontSize="xs" px={4} py={2} fontWeight="bold">
        Menu
      </Text>
      <Box>{listItems}</Box>
    </>
  )
}

export default SidebarItems
