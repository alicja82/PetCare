<template>
  <div class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ schedule ? 'Edytuj harmonogram' : 'Dodaj harmonogram karmienia' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <!-- Pet selection -->
            <div class="mb-3" v-if="!schedule && pets.length > 0">
              <label class="form-label">Zwierzę *</label>
              <select class="form-select" v-model="form.pet_id" required>
                <option value="">Wybierz zwierzę...</option>
                <option v-for="pet in pets" :key="pet.id" :value="pet.id">
                  {{ pet.name }}
                </option>
              </select>
            </div>

            <!-- Food type -->
            <div class="mb-3">
              <label class="form-label">Rodzaj karmy *</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="form.food_type"
                placeholder="np. Karma sucha dla psów"
                required
              />
            </div>

            <!-- Amount -->
            <div class="mb-3">
              <label class="form-label">Ilość *</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="form.amount"
                placeholder="np. 200g, 1 kubek"
                required
              />
            </div>

            <!-- Feeding time -->
            <div class="mb-3">
              <label class="form-label">Godzina karmienia *</label>
              <input 
                type="time" 
                class="form-control" 
                v-model="form.feeding_time"
                required
              />
            </div>

            <!-- Frequency -->
            <div class="mb-3">
              <label class="form-label">Częstotliwość</label>
              <select class="form-select" v-model="form.frequency">
                <option value="Codziennie">Codziennie</option>
                <option value="Co drugi dzień">Co drugi dzień</option>
                <option value="Raz w tygodniu">Raz w tygodniu</option>
                <option value="Weekendy">Weekendy</option>
                <option value="Dni robocze">Dni robocze</option>
              </select>
            </div>

            <!-- Notes -->
            <div class="mb-3">
              <label class="form-label">Notatki</label>
              <textarea 
                class="form-control" 
                v-model="form.notes"
                rows="3"
                placeholder="Dodatkowe informacje..."
              ></textarea>
            </div>

            <div class="text-end">
              <button type="button" class="btn btn-secondary me-2" @click="$emit('close')">
                Anuluj
              </button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ schedule ? 'Zapisz' : 'Dodaj' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useScheduleStore } from '../stores/schedule'

const props = defineProps({
  schedule: Object,
  pets: Array,
  selectedPetId: Number
})

const emit = defineEmits(['close', 'save'])

const scheduleStore = useScheduleStore()
const loading = ref(false)

const form = ref({
  pet_id: props.selectedPetId || (props.schedule?.pet_id || ''),
  food_type: props.schedule?.food_type || '',
  amount: props.schedule?.amount || '',
  feeding_time: props.schedule?.feeding_time || '',
  frequency: props.schedule?.frequency || 'Codziennie',
  notes: props.schedule?.notes || ''
})

watch(() => props.selectedPetId, (newVal) => {
  if (newVal && !props.schedule) {
    form.value.pet_id = newVal
  }
})

const handleSubmit = async () => {
  loading.value = true
  try {
    if (props.schedule) {
      // Update existing schedule
      await scheduleStore.updateSchedule(props.schedule.id, form.value)
    } else {
      // Create new schedule
      await scheduleStore.createSchedule(form.value.pet_id, form.value)
    }
    emit('save')
  } catch (error) {
    // Error is handled in store
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal.show {
  display: block;
}
</style>
