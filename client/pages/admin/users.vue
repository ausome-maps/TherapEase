<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-col sm:flex-row gap-3 sm:gap-0">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Users</h2>
        <p class="mt-1 text-sm text-gray-600">Manage all registered users</p>
      </div>
      <button @click="openCreateModal"
        class="px-4 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500 text-sm font-medium w-full sm:w-auto">
        Create User
      </button>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      {{ error }}
    </div>
    <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
      {{ success }}
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin text-4xl text-red-400">&#9696;</div>
      <p class="mt-4 text-gray-600">Loading users...</p>
    </div>

    <div v-else class="bg-white shadow rounded-lg overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            <th class="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Joined</th>
            <th class="px-3 sm:px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">
                {{ user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` : '—' }}
              </div>
              <div class="text-xs sm:text-sm text-gray-500">{{ user.email }}</div>
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
              <span v-if="user.is_superuser" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                Superuser
              </span>
              <span v-else-if="user.is_staff" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Staff
              </span>
              <span v-else class="text-xs sm:text-sm text-gray-500">User</span>
            </td>
            <td class="hidden sm:table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(user.date_joined) }}
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-right text-xs sm:text-sm font-medium">
              <button @click="openEditModal(user)" class="text-red-400 hover:text-red-500 mr-1 sm:mr-3">Edit</button>
              <button @click="toggleActive(user)" class="text-gray-400 hover:text-gray-500 mr-1 sm:mr-3">
                {{ user.is_active ? 'Disable' : 'Enable' }}
              </button>
              <button @click="confirmDelete(user)" class="text-red-600 hover:text-red-800">Delete</button>
            </td>
          </tr>
          <tr v-if="users.length === 0">
            <td colspan="5" class="px-6 py-12 text-center text-gray-500">No users found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6 space-y-4">
        <h3 class="text-xl font-bold text-gray-900">{{ editingUser ? 'Edit User' : 'Create User' }}</h3>

        <div v-if="modalError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {{ modalError }}
        </div>

        <form @submit.prevent="handleCreateOrEdit" class="space-y-4">
          <div>
            <label for="modalEmail" class="block text-sm font-medium text-gray-700">Email</label>
            <input id="modalEmail" v-model="modalEmail" type="email" required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
          </div>
          <div v-if="!editingUser">
            <label for="modalPassword" class="block text-sm font-medium text-gray-700">Password</label>
            <input id="modalPassword" v-model="modalPassword" type="password" required minlength="8"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
          </div>
          <div>
            <label for="modalFirstName" class="block text-sm font-medium text-gray-700">First Name</label>
            <input id="modalFirstName" v-model="modalFirstName" type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
          </div>
          <div>
            <label for="modalLastName" class="block text-sm font-medium text-gray-700">Last Name</label>
            <input id="modalLastName" v-model="modalLastName" type="text"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
          </div>
          <div v-if="editingUser" class="flex items-center gap-6">
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="modalIsActive" class="rounded border-gray-300">
              <span class="text-sm text-gray-700">Active</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="modalIsStaff" class="rounded border-gray-300">
              <span class="text-sm text-gray-700">Staff</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="modalIsSuperuser" class="rounded border-gray-300">
              <span class="text-sm text-gray-700">Superuser</span>
            </label>
          </div>
          <div class="flex gap-3 pt-2">
            <button type="submit" :disabled="modalSaving"
              class="flex-1 py-2 px-4 bg-red-400 text-white rounded-lg hover:bg-red-500 disabled:opacity-50 text-sm font-medium">
              {{ modalSaving ? 'Saving...' : (editingUser ? 'Update' : 'Create') }}
            </button>
            <button type="button" @click="closeModal"
              class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-medium">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-sm w-full p-6 space-y-4">
        <h3 class="text-xl font-bold text-gray-900">Delete User</h3>
        <p class="text-gray-600 text-sm">
          Are you sure you want to delete <strong>{{ deletingUser?.email }}</strong>? This action cannot be undone.
        </p>
        <div class="flex gap-3">
          <button @click="handleDelete"
            class="flex-1 py-2 px-4 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium">
            Delete
          </button>
          <button @click="showDeleteModal = false"
            class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-medium">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

definePageMeta({ layout: 'admin' })

interface AdminUser {
  id: number
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  is_staff: boolean
  is_superuser: boolean
  date_joined: string
}

const { isStaff, isSuperuser, initAuth, fetchUsers, createUser, updateUser, deleteUser } = useAuth()

const users = ref<AdminUser[]>([])
const loading = ref(true)
const error = ref('')
const success = ref('')

const showModal = ref(false)
const showDeleteModal = ref(false)
const editingUser = ref<AdminUser | null>(null)
const deletingUser = ref<AdminUser | null>(null)
const modalEmail = ref('')
const modalPassword = ref('')
const modalFirstName = ref('')
const modalLastName = ref('')
const modalIsActive = ref(true)
const modalIsStaff = ref(false)
const modalIsSuperuser = ref(false)
const modalError = ref('')
const modalSaving = ref(false)

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleDateString()
}

const loadUsers = async () => {
  try {
    const data = await fetchUsers()
    users.value = data.results
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await initAuth()
  if (!isStaff.value && !isSuperuser.value) {
    loading.value = false
    return
  }
  await loadUsers()
})

const openCreateModal = () => {
  editingUser.value = null
  modalEmail.value = ''
  modalPassword.value = ''
  modalFirstName.value = ''
  modalLastName.value = ''
  modalError.value = ''
  showModal.value = true
}

const openEditModal = (user: AdminUser) => {
  editingUser.value = user
  modalEmail.value = user.email
  modalFirstName.value = user.first_name
  modalLastName.value = user.last_name
  modalIsActive.value = user.is_active
  modalIsStaff.value = user.is_staff
  modalIsSuperuser.value = user.is_superuser
  modalPassword.value = ''
  modalError.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingUser.value = null
}

const handleCreateOrEdit = async () => {
  modalError.value = ''
  modalSaving.value = true
  try {
    if (editingUser.value) {
      await updateUser(editingUser.value.id, {
        email: modalEmail.value,
        first_name: modalFirstName.value,
        last_name: modalLastName.value,
        is_active: modalIsActive.value,
        is_staff: modalIsStaff.value,
        is_superuser: modalIsSuperuser.value,
      })
      success.value = 'User updated successfully!'
    } else {
      const created = await createUser(modalEmail.value, modalPassword.value)
      const createdId = created.id || created.data?.id
      if (createdId && (modalFirstName.value || modalLastName.value)) {
        try {
          await updateUser(createdId, {
            first_name: modalFirstName.value,
            last_name: modalLastName.value,
          })
        } catch {}
      }
      success.value = 'User created successfully!'
    }
    closeModal()
    await loadUsers()
    setTimeout(() => { success.value = '' }, 3000)
  } catch (e: any) {
    modalError.value = e.message
  } finally {
    modalSaving.value = false
  }
}

const toggleActive = async (user: AdminUser) => {
  try {
    await updateUser(user.id, { is_active: !user.is_active })
    user.is_active = !user.is_active
    success.value = `User ${user.is_active ? 'enabled' : 'disabled'} successfully!`
    setTimeout(() => { success.value = '' }, 3000)
  } catch (e: any) {
    error.value = e.message
  }
}

const confirmDelete = (user: AdminUser) => {
  deletingUser.value = user
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!deletingUser.value) return
  try {
    await deleteUser(deletingUser.value.id)
    users.value = users.value.filter((u) => u.id !== deletingUser.value!.id)
    success.value = 'User deleted successfully!'
    showDeleteModal.value = false
    deletingUser.value = null
    setTimeout(() => { success.value = '' }, 3000)
  } catch (e: any) {
    error.value = e.message
    showDeleteModal.value = false
  }
}
</script>
