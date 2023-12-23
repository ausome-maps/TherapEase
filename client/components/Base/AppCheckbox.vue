<template>
    <div class="checkbox-container">
        <input :id="id_" type="checkbox" v-model="model" class="checkbox-input">
        <label :for="id_" class="checkbox-label">{{label}}</label>
    </div>
</template>


<script>
export default {
    props: {
        label: {
            type: String,
            required: true
        },
        id_: {
            type: String,
            required: true
        },
        modelValue: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        model: {
            get() {
                return this.modelValue;
            },
            set(value) {
                this.$emit('update:modelValue', value);
            }
        }
    }
}
</script>



<style scoped>
.checkbox-container {
    display: flex;
    align-items: center;
}

.checkbox-input {
    border-radius: 5px;
    width: 20px;
    height: 20px;
    margin-right: 10px;
    cursor: pointer;
    appearance: none;
    background-color: #fff;
    border: 2px solid #333;
    box-sizing: border-box;
    position: relative;
    outline: none;
    padding: 5px;

}

.checkbox-input:checked {
    background-color: #000;
    border-color: #333;
    ;

}

.checkbox-input:checked::after {
    content: "";
    display: block;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    position: absolute;
    transform: rotate(45deg);
    top: 10%;
    left: 35%;

}

.checkbox-label {
    font-size: 16px;
    color: #333;
    cursor: pointer;
}
</style>
