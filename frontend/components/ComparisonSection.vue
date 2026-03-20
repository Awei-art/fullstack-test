<script setup>
import { ref, onUnmounted } from 'vue'

const { getByKey } = await useSiteImages()

const containerRef = ref(null)
const sliderValue = ref(50) // Default 50%
let isDragging = false

const updateSlider = (clientX) => {
    if (!containerRef.value) return

    const rect = containerRef.value.getBoundingClientRect()
    let posX = clientX - rect.left

    // Clamp
    if (posX < 0) posX = 0
    if (posX > rect.width) posX = rect.width

    // Calculate percentage (0 to 100)
    sliderValue.value = (posX / rect.width) * 100
}

const onMouseMove = (e) => {
    if (!isDragging) return
    updateSlider(e.clientX)
}

const onTouchMove = (e) => {
    if (!isDragging) return
    updateSlider(e.touches[0].clientX)
}

const stopDrag = () => {
    isDragging = false
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', stopDrag)
    window.removeEventListener('touchmove', onTouchMove)
    window.removeEventListener('touchend', stopDrag)
}

const startDrag = (e) => {
    isDragging = true
    
    // Handle initial click/touch position update
    if (e.type === 'mousedown') {
        updateSlider(e.clientX)
        window.addEventListener('mousemove', onMouseMove)
        window.addEventListener('mouseup', stopDrag)
    } else if (e.type === 'touchstart') {
        updateSlider(e.touches[0].clientX)
        window.addEventListener('touchmove', onTouchMove)
        window.addEventListener('touchend', stopDrag)
    }
}

// Ensure cleanup
onUnmounted(() => {
    if (typeof window !== 'undefined') {
        window.removeEventListener('mousemove', onMouseMove)
        window.removeEventListener('mouseup', stopDrag)
        window.removeEventListener('touchmove', onTouchMove)
        window.removeEventListener('touchend', stopDrag)
    }
})
</script>

<template>
    <section class="comparison_section">
        <div class="comparison_container">
            <h2 class="comparison_title">甜點與葡萄的完美結合</h2>
            <div 
                class="comparison_wrapper" 
                ref="containerRef"
                @mousedown="startDrag" 
                @touchstart="startDrag"
            >
                <!-- Back Image (Right Side: Mochi 01) -->
                <img :src="getByKey('comparison_right', '/images/mochi01.png')" alt="Mochi 01" class="comp-img comp-img-back">

                <!-- Front Image (Left Side: Mochi 02) -->
                <img 
                    :src="getByKey('comparison_left', '/images/mochi02.png')" 
                    alt="Mochi 02" 
                    class="comp-img comp-img-front"
                    :style="{ clipPath: `inset(0 ${100 - sliderValue}% 0 0)` }"
                >

                <!-- Handle -->
                <div 
                    class="comp-handle"
                    :style="{ left: `${sliderValue}%` }"
                >
                    <i class="fas fa-arrows-alt-h"></i>
                </div>
            </div>

        </div>
    </section>
</template>

<style src="@/assets/css/ComparisonSection.css" scoped></style>
