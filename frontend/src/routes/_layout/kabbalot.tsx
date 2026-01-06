import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Table,
  VStack,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { FiSearch } from "react-icons/fi"

import { KabbalotService } from "@/client"
import { KabbalahActionsMenu } from "@/components/Common/KabbalahActionsMenu"
import AddKabbalah from "@/components/Kabbalot/AddKabbalah"

function getKabbalotQueryOptions() {
  return {
    queryFn: () => KabbalotService.listKabbalot(),
    queryKey: ["kabbalot"],
  }
}

export const Route = createFileRoute("/_layout/kabbalot")({
  component: Kabbalot,
})

function KabbalotTable() {
  const { data, isLoading } = useQuery(getKabbalotQueryOptions())

  const kabbalot = data ?? []

  if (isLoading) {
    return (
      <Flex justify="center" align="center" h="200px">
        Loading...
      </Flex>
    )
  }

  if (kabbalot.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any kabbalot yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new kabbalah to get started
            </EmptyState.Description>
          </VStack>
        </EmptyState.Content>
      </EmptyState.Root>
    )
  }

  return (
    <Table.Root size={{ base: "sm", md: "md" }}>
      <Table.Header>
        <Table.Row>
          <Table.ColumnHeader w="sm">ID</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Middah</Table.ColumnHeader>
          <Table.ColumnHeader>Description</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {kabbalot.map((kabbalah) => (
          <Table.Row key={kabbalah.id}>
            <Table.Cell truncate maxW="sm">
              {kabbalah.id}
            </Table.Cell>
            <Table.Cell truncate maxW="sm">
              {kabbalah.middah}
            </Table.Cell>
            <Table.Cell truncate maxW="lg">
              "{kabbalah.description}"
            </Table.Cell>
            <Table.Cell>
              <KabbalahActionsMenu kabbalah={kabbalah} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}

function Kabbalot() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Kabbalot Management
      </Heading>
      <AddKabbalah />
      <KabbalotTable />
    </Container>
  )
}

export default Kabbalot
