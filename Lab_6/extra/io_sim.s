	.file	"io_sim.c"
	.text
	.p2align 4
	.type	state_free, @function
state_free:
.LFB56:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movq	%rdi, %rbx
	movq	8(%rdi), %rdi
	call	free@PLT
	movq	16(%rbx), %rdi
	call	free@PLT
	movq	24(%rbx), %rdi
	call	free@PLT
	movq	32(%rbx), %rdi
	call	free@PLT
	movq	40(%rbx), %rdi
	call	free@PLT
	movq	48(%rbx), %rdi
	call	free@PLT
	movq	56(%rbx), %rdi
	call	free@PLT
	movq	64(%rbx), %rdi
	call	free@PLT
	movq	72(%rbx), %rdi
	call	free@PLT
	movq	80(%rbx), %rdi
	call	free@PLT
	movq	88(%rbx), %rdi
	call	free@PLT
	movq	96(%rbx), %rdi
	call	free@PLT
	movq	104(%rbx), %rdi
	call	free@PLT
	movq	112(%rbx), %rdi
	call	free@PLT
	movq	120(%rbx), %rdi
	popq	%rbx
	.cfi_def_cfa_offset 8
	jmp	free@PLT
	.cfi_endproc
.LFE56:
	.size	state_free, .-state_free
	.p2align 4
	.type	state_init.constprop.0, @function
state_init.constprop.0:
.LFB60:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	movq	%rdi, %rbp
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	movslq	%esi, %rbx
	movq	%rbx, %r12
	subq	$120, %rsp
	.cfi_def_cfa_offset 176
	movl	%ebx, (%rdi)
	salq	$2, %rbx
	movl	$64, %edi
	movq	%rbx, %rsi
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 8(%rbp)
	movq	%rax, 8(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 16(%rbp)
	movq	%rax, 16(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 24(%rbp)
	movq	%rax, 24(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 32(%rbp)
	movq	%rax, 32(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 40(%rbp)
	movq	%rax, 40(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 48(%rbp)
	movq	%rax, 48(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 56(%rbp)
	movq	%rax, 56(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 64(%rbp)
	movq	%rax, 64(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 72(%rbp)
	movq	%rax, 72(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 80(%rbp)
	movq	%rax, 80(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 88(%rbp)
	movq	%rax, 88(%rsp)
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 96(%rbp)
	movq	%rax, %r13
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 104(%rbp)
	movq	%rax, %r14
	call	aligned_alloc@PLT
	movq	%rbx, %rsi
	movl	$64, %edi
	movq	%rax, 112(%rbp)
	movq	%rax, %r15
	call	aligned_alloc@PLT
	testl	%r12d, %r12d
	movq	%rax, 120(%rbp)
	jle	.L7
	movl	$1981, %edx
	movq	%rbx, 96(%rsp)
	vmovss	.LC0(%rip), %xmm0
	vxorps	%xmm10, %xmm10, %xmm10
	movq	%rax, 104(%rsp)
	vmovss	.LC1(%rip), %xmm11
	xorl	%r12d, %r12d
	movl	%edx, %ebx
	vmovss	.LC4(%rip), %xmm13
	vmovss	.LC5(%rip), %xmm14
	vmovss	.LC9(%rip), %xmm12
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L9:
	movl	%ebx, %r11d
	vmovss	.LC16(%rip), %xmm2
	sall	$13, %r11d
	xorl	%ebx, %r11d
	movl	%r11d, %ebp
	shrl	$17, %ebp
	xorl	%r11d, %ebp
	movl	%ebp, %edx
	sall	$5, %edx
	xorl	%ebp, %edx
	movl	%edx, %ecx
	movl	%edx, %ebp
	shrl	$8, %ecx
	vcvtsi2ssl	%ecx, %xmm10, %xmm0
	vfmadd132ss	.LC15(%rip), %xmm2, %xmm0
	call	logf@PLT
	movl	%ebp, %eax
	vxorps	%xmm5, %xmm5, %xmm5
	vmulss	.LC17(%rip), %xmm0, %xmm3
	sall	$13, %eax
	xorl	%ebp, %eax
	movl	%eax, %esi
	shrl	$17, %eax
	xorl	%esi, %eax
	movl	%eax, %edi
	sall	$5, %edi
	vsqrtss	%xmm3, %xmm3, %xmm4
	xorl	%eax, %edi
	shrl	$8, %edi
	vcvtsi2ssl	%edi, %xmm5, %xmm9
	vmulss	.LC18(%rip), %xmm9, %xmm0
	vmovss	%xmm4, 4(%rsp)
	call	cosf@PLT
	vmovss	4(%rsp), %xmm11
	vmovss	.LC9(%rip), %xmm12
	vxorps	%xmm10, %xmm10, %xmm10
	vmovss	.LC4(%rip), %xmm13
	vmovss	.LC5(%rip), %xmm14
.L6:
	movl	%ebx, %edx
	vmovss	.LC3(%rip), %xmm6
	movq	8(%rsp), %r9
	movl	$0x406dc28f, 0(%r13,%r12)
	vmulss	%xmm0, %xmm11, %xmm0
	sall	$13, %edx
	movl	$0x3c3923a3, (%r14,%r12)
	xorl	%ebx, %edx
	movl	$0x3ba1844a, (%r15,%r12)
	vfmadd132ss	.LC2(%rip), %xmm6, %xmm0
	movl	%edx, %ecx
	shrl	$17, %ecx
	xorl	%ecx, %edx
	movl	%edx, %eax
	sall	$5, %eax
	vmovss	%xmm0, (%r9,%r12)
	xorl	%eax, %edx
	movl	%edx, %esi
	sall	$13, %esi
	xorl	%edx, %esi
	movq	16(%rsp), %rdx
	movl	%esi, %edi
	shrl	$17, %edi
	xorl	%edi, %esi
	movl	%esi, %r8d
	sall	$5, %r8d
	xorl	%r8d, %esi
	movq	24(%rsp), %r8
	movl	%esi, %r10d
	sall	$13, %r10d
	xorl	%esi, %r10d
	movl	%r10d, %r11d
	shrl	$17, %r11d
	xorl	%r11d, %r10d
	movl	%r10d, %ebp
	sall	$5, %ebp
	xorl	%ebp, %r10d
	movq	32(%rsp), %rbp
	movl	%r10d, %ecx
	movl	%r10d, %ebx
	sall	$13, %ecx
	shrl	$8, %ebx
	xorl	%r10d, %ecx
	vcvtsi2ssl	%ebx, %xmm10, %xmm1
	movl	%ecx, %eax
	shrl	$17, %eax
	xorl	%eax, %ecx
	movq	56(%rsp), %rax
	movl	%ecx, %esi
	vfmadd132ss	%xmm13, %xmm14, %xmm1
	sall	$5, %esi
	movl	$0x3eb81e5b, (%rax,%r12)
	xorl	%esi, %ecx
	movq	64(%rsp), %rsi
	movl	%ecx, %ebx
	movl	%ecx, %edi
	sall	$13, %ebx
	shrl	$8, %edi
	vmovss	%xmm12, (%rsi,%r12)
	xorl	%ecx, %ebx
	vcvtsi2ssl	%edi, %xmm10, %xmm7
	vmovss	%xmm1, (%rdx,%r12)
	movq	48(%rsp), %rcx
	movl	%ebx, %r9d
	movq	40(%rsp), %rdx
	movq	72(%rsp), %rdi
	shrl	$17, %r9d
	movl	$0x3d039fe3, (%rcx,%r12)
	xorl	%r9d, %ebx
	movq	88(%rsp), %r9
	movl	$0x3f3e086a, (%rdx,%r12)
	movl	%ebx, %r10d
	vfmadd132ss	%xmm13, %xmm14, %xmm7
	movl	$0x3dcccccd, (%rdi,%r12)
	sall	$5, %r10d
	vmovss	%xmm12, (%r9,%r12)
	xorl	%r10d, %ebx
	movq	104(%rsp), %r10
	movl	%ebx, %r11d
	shrl	$8, %r11d
	movl	$0x3d0a60ac, (%r10,%r12)
	vcvtsi2ssl	%r11d, %xmm10, %xmm8
	vmovss	%xmm7, (%r8,%r12)
	movq	80(%rsp), %r8
	movl	$0x3f666666, (%r8,%r12)
	vfmadd132ss	%xmm13, %xmm14, %xmm8
	vmovss	%xmm8, 0(%rbp,%r12)
	addq	$4, %r12
	cmpq	%r12, 96(%rsp)
	jne	.L9
.L7:
	addq	$120, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE60:
	.size	state_init.constprop.0, .-state_init.constprop.0
	.p2align 4
	.type	run_sim._omp_fn.0, @function
run_sim._omp_fn.0:
.LFB59:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	andq	$-32, %rsp
	subq	$896, %rsp
	.cfi_offset 15, -24
	.cfi_offset 14, -32
	.cfi_offset 13, -40
	.cfi_offset 12, -48
	.cfi_offset 3, -56
	movq	120(%rdi), %rax
	movq	112(%rdi), %rdx
	movq	104(%rdi), %rcx
	movq	96(%rdi), %rbx
	movq	80(%rdi), %rsi
	movq	72(%rdi), %r8
	movq	%rax, 360(%rsp)
	vmovss	152(%rdi), %xmm2
	movq	64(%rdi), %r9
	movq	%rdx, 96(%rsp)
	movq	%rcx, 352(%rsp)
	movq	88(%rdi), %r15
	movq	%rbx, 88(%rsp)
	movq	%rsi, 80(%rsp)
	movq	%r8, 72(%rsp)
	movq	%r9, 64(%rsp)
	vmovss	%xmm2, 372(%rsp)
	movq	56(%rdi), %r10
	movq	(%rdi), %rbx
	movq	48(%rdi), %r11
	movq	40(%rdi), %r12
	movq	32(%rdi), %r13
	movq	24(%rdi), %r14
	movq	%r10, 56(%rsp)
	movq	16(%rdi), %rax
	movq	8(%rdi), %rdx
	movq	%r11, 48(%rsp)
	movl	148(%rdi), %ecx
	vmovss	140(%rdi), %xmm1
	movq	%r12, 40(%rsp)
	movl	136(%rdi), %esi
	vmovss	132(%rdi), %xmm3
	movq	%r13, 32(%rsp)
	vmovss	144(%rdi), %xmm0
	movslq	128(%rdi), %rdi
	movq	%r14, 752(%rsp)
	movq	%rax, 536(%rsp)
	testl	%edi, %edi
	movq	%rdx, 744(%rsp)
	movl	%ecx, 124(%rsp)
	movl	%esi, 120(%rsp)
	vmovss	%xmm1, 112(%rsp)
	vmovss	%xmm3, 764(%rsp)
	jle	.L99
	vmovss	.LC25(%rip), %xmm8
	vmulss	.LC21(%rip), %xmm0, %xmm6
	leaq	(%rbx,%rdi,4), %r8
	movq	%rbx, 376(%rsp)
	vmulss	.LC22(%rip), %xmm0, %xmm4
	movq	%r8, 104(%rsp)
	movl	$0x00000000, 740(%rsp)
	vmulss	%xmm3, %xmm8, %xmm9
	vmulss	.LC23(%rip), %xmm3, %xmm5
	vmulss	.LC24(%rip), %xmm3, %xmm7
	vmovss	%xmm6, 116(%rsp)
	vmovss	%xmm4, 12(%rsp)
	vmovss	%xmm9, 368(%rsp)
	vmovss	%xmm5, 344(%rsp)
	vmovss	%xmm7, 348(%rsp)
	.p2align 4,,10
	.p2align 3
.L36:
	call	GOMP_single_start@PLT
	testb	%al, %al
	je	.L42
	movq	$0x000000000, sigma.0(%rip)
.L42:
	call	GOMP_barrier@PLT
	call	omp_get_num_threads@PLT
	movl	%eax, %r12d
	call	omp_get_thread_num@PLT
	movl	%eax, %r9d
	movl	124(%rsp), %eax
	cltd
	idivl	%r12d
	cmpl	%edx, %r9d
	movl	%edx, 736(%rsp)
	movl	%eax, %r14d
	jl	.L13
.L41:
	imull	%r14d, %r9d
	movl	736(%rsp), %r10d
	vxorpd	%xmm13, %xmm13, %xmm13
	addl	%r9d, %r10d
	movl	%r9d, 512(%rsp)
	leal	(%r14,%r10), %r11d
	movl	%r10d, 524(%rsp)
	cmpl	%r11d, %r10d
	movl	%r11d, 760(%rsp)
	jl	.L101
.L14:
	movq	sigma.0(%rip), %r10
.L21:
	movq	%r10, %rax
	lock cmpxchgq	%r10, sigma.0(%rip)
	jne	.L45
	vaddsd	sigma.0(%rip), %xmm13, %xmm14
	vmovsd	%xmm14, sigma.0(%rip)
	call	GOMP_barrier@PLT
	movl	120(%rsp), %r11d
	testl	%r11d, %r11d
	jne	.L22
	movl	$0x00000000, 520(%rsp)
.L40:
	vmovss	740(%rsp), %xmm3
	vcomiss	116(%rsp), %xmm3
	ja	.L23
	movl	$0x00000000, 516(%rsp)
.L38:
	movl	760(%rsp), %r13d
	cmpl	%r13d, 524(%rsp)
	jl	.L24
.L30:
	call	GOMP_barrier@PLT
	call	GOMP_single_start@PLT
	testb	%al, %al
	je	.L102
	movq	744(%rsp), %r14
	movq	376(%rsp), %rbx
	vmovss	(%r14), %xmm0
	addq	$4, %rbx
	vmovss	%xmm0, -4(%rbx)
	call	GOMP_barrier@PLT
	movq	104(%rsp), %r8
	vmovss	740(%rsp), %xmm2
	movq	%rbx, 376(%rsp)
	vaddss	764(%rsp), %xmm2, %xmm9
	cmpq	%r8, %rbx
	vmovss	%xmm9, 740(%rsp)
	jne	.L36
.L99:
	leaq	-40(%rbp), %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_remember_state
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L102:
	.cfi_restore_state
	call	GOMP_barrier@PLT
	vmovss	740(%rsp), %xmm4
	vaddss	764(%rsp), %xmm4, %xmm3
	addq	$4, 376(%rsp)
	movq	376(%rsp), %rax
	cmpq	%rax, 104(%rsp)
	vmovss	%xmm3, 740(%rsp)
	jne	.L36
	leaq	-40(%rbp), %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_remember_state
	.cfi_def_cfa 7, 8
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	.cfi_restore_state
	vmovss	12(%rsp), %xmm6
	vmovss	112(%rsp), %xmm1
	vxorps	%xmm5, %xmm5, %xmm5
	vxorps	.LC249(%rip), %xmm1, %xmm4
	vcmpltss	%xmm6, %xmm3, %xmm0
	vblendvps	%xmm0, %xmm4, %xmm5, %xmm7
	vmovss	%xmm7, 516(%rsp)
	jmp	.L38
	.p2align 4,,10
	.p2align 3
.L22:
	vxorps	%xmm15, %xmm15, %xmm15
	vcvtsd2ss	sigma.0(%rip), %xmm15, %xmm2
	vmovss	%xmm2, 520(%rsp)
	jmp	.L40
	.p2align 4,,10
	.p2align 3
.L24:
	leal	-1(%r14), %ecx
	cmpl	$6, %ecx
	jbe	.L46
	movslq	736(%rsp), %rbx
	movslq	512(%rsp), %rdx
	movq	744(%rsp), %rsi
	movq	536(%rsp), %r8
	movq	360(%rsp), %rdi
	addq	%rbx, %rdx
	movq	40(%rsp), %rax
	salq	$2, %rdx
	movq	32(%rsp), %r9
	movq	48(%rsp), %r10
	addq	%rdx, %rsi
	addq	%rdx, %r8
	addq	%rdx, %rdi
	movq	72(%rsp), %rcx
	movq	%rsi, 640(%rsp)
	leaq	(%rax,%rdx), %rsi
	movq	352(%rsp), %rax
	leaq	(%r9,%rdx), %r13
	movq	%r8, 768(%rsp)
	movq	80(%rsp), %r8
	movq	%rdi, 336(%rsp)
	movq	88(%rsp), %rdi
	movq	56(%rsp), %rbx
	movq	752(%rsp), %r12
	leaq	(%r8,%rdx), %r9
	movq	64(%rsp), %r11
	leaq	(%rdi,%rdx), %r8
	leaq	(%rax,%rdx), %rdi
	movq	96(%rsp), %rax
	vbroadcastss	764(%rsp), %ymm8
	addq	%rdx, %r12
	addq	%rdx, %rbx
	vbroadcastss	520(%rsp), %ymm13
	vbroadcastss	344(%rsp), %ymm9
	leaq	(%r11,%rdx), %r11
	vbroadcastss	348(%rsp), %ymm10
	movq	%r12, 528(%rsp)
	vbroadcastss	368(%rsp), %ymm11
	leaq	(%r10,%rdx), %r12
	vbroadcastss	372(%rsp), %ymm12
	leaq	(%rcx,%rdx), %r10
	vmovaps	%ymm8, 704(%rsp)
	leaq	(%r15,%rdx), %rcx
	addq	%rax, %rdx
	movl	%r14d, %eax
	vmovaps	%ymm13, 160(%rsp)
	shrl	$3, %eax
	vmovaps	%ymm9, 288(%rsp)
	salq	$5, %rax
	vmovaps	%ymm10, 256(%rsp)
	vmovaps	%ymm11, 224(%rsp)
	vmovaps	%ymm12, 192(%rsp)
	vbroadcastss	516(%rsp), %ymm14
	vbroadcastss	.LC31(%rip), %ymm15
	vbroadcastss	.LC33(%rip), %ymm2
	movl	%r14d, 8(%rsp)
	vbroadcastss	.LC41(%rip), %ymm3
	movq	%r15, (%rsp)
	vbroadcastss	.LC43(%rip), %ymm6
	vbroadcastss	.LC104(%rip), %ymm7
	movq	%rax, 328(%rsp)
	xorl	%eax, %eax
	vbroadcastss	.LC62(%rip), %ymm4
	vbroadcastss	.LC78(%rip), %ymm5
	vmovaps	%ymm14, 128(%rsp)
	vbroadcastss	.LC110(%rip), %ymm8
	vmovaps	%ymm15, 608(%rsp)
	vbroadcastss	.LC45(%rip), %ymm0
	vmovaps	%ymm2, 480(%rsp)
	vbroadcastss	.LC51(%rip), %ymm14
	vbroadcastss	.LC53(%rip), %ymm15
	vmovaps	%ymm3, 832(%rsp)
	vbroadcastss	.LC55(%rip), %ymm13
	vbroadcastss	.LC49(%rip), %ymm3
	vmovaps	%ymm6, 864(%rsp)
	vbroadcastss	.LC57(%rip), %ymm2
	vbroadcastss	.LC47(%rip), %ymm6
	movq	768(%rsp), %r14
	movq	640(%rsp), %r15
	vmovaps	%ymm7, 576(%rsp)
	vbroadcastss	.LC59(%rip), %ymm1
	vpbroadcastd	.LC250(%rip), %ymm7
	vmovaps	%ymm4, 800(%rsp)
	vmovaps	%ymm5, 672(%rsp)
	vmovaps	%ymm8, 544(%rsp)
	movq	%rdi, 320(%rsp)
	.p2align 4,,10
	.p2align 3
.L28:
	vmovups	(%r15,%rax), %ymm5
	vmovups	(%r14,%rax), %ymm10
	movq	528(%rsp), %rdi
	vaddps	608(%rsp), %ymm5, %ymm8
	vmovaps	%ymm10, 768(%rsp)
	vsubps	%ymm10, %ymm5, %ymm12
	vmovups	0(%r13,%rax), %ymm10
	vmulps	.LC26(%rip), %ymm12, %ymm4
	vmovups	(%rdi,%rax), %ymm9
	movq	336(%rsp), %rdi
	vmovaps	%ymm9, 640(%rsp)
	vsubps	%ymm9, %ymm5, %ymm11
	vmulps	%ymm10, %ymm10, %ymm9
	vfmadd132ps	.LC28(%rip), %ymm4, %ymm11
	vmulps	%ymm10, %ymm9, %ymm12
	vaddps	480(%rsp), %ymm5, %ymm10
	vmulps	(%rsi,%rax), %ymm12, %ymm4
	vmulps	(%rdi,%rax), %ymm4, %ymm9
	vmulps	%ymm10, %ymm9, %ymm12
	vfmadd132ps	.LC34(%rip), %ymm12, %ymm8
	vmovaps	832(%rsp), %ymm12
	vaddps	%ymm8, %ymm11, %ymm11
	vaddps	.LC36(%rip), %ymm5, %ymm8
	vmulps	.LC38(%rip), %ymm8, %ymm4
	vmovaps	%ymm11, 448(%rsp)
	vmovaps	864(%rsp), %ymm11
	vminps	%ymm12, %ymm4, %ymm9
	vmaxps	%ymm11, %ymm9, %ymm4
	vmovaps	%ymm4, %ymm10
	vfmadd132ps	%ymm0, %ymm6, %ymm10
	vroundps	$9, %ymm10, %ymm8
	vfmsub132ps	%ymm0, %ymm8, %ymm4
	vcvttps2dq	%ymm8, %ymm9
	vmovaps	%ymm4, %ymm10
	vfmadd132ps	%ymm3, %ymm14, %ymm10
	vfmadd132ps	%ymm4, %ymm15, %ymm10
	vfmadd132ps	%ymm4, %ymm13, %ymm10
	vfmadd132ps	%ymm4, %ymm2, %ymm10
	vfmadd132ps	%ymm4, %ymm1, %ymm10
	vpaddd	%ymm7, %ymm9, %ymm4
	vaddps	.LC63(%rip), %ymm5, %ymm9
	vpslld	$23, %ymm4, %ymm8
	vfmadd213ps	800(%rsp), %ymm8, %ymm10
	vmulps	.LC65(%rip), %ymm9, %ymm4
	vminps	%ymm12, %ymm4, %ymm8
	vmaxps	%ymm11, %ymm8, %ymm4
	vmovaps	%ymm4, %ymm9
	vfmadd132ps	%ymm0, %ymm6, %ymm9
	vroundps	$9, %ymm9, %ymm8
	vfmsub132ps	%ymm0, %ymm8, %ymm4
	vmovaps	%ymm4, %ymm9
	vfmadd132ps	%ymm3, %ymm14, %ymm9
	vfmadd132ps	%ymm4, %ymm15, %ymm9
	vfmadd132ps	%ymm4, %ymm13, %ymm9
	vfmadd132ps	%ymm4, %ymm2, %ymm9
	vfmadd132ps	%ymm4, %ymm1, %ymm9
	vcvttps2dq	%ymm8, %ymm4
	vpaddd	%ymm7, %ymm4, %ymm8
	vpslld	$23, %ymm8, %ymm4
	vaddps	.LC67(%rip), %ymm5, %ymm8
	vfmadd213ps	800(%rsp), %ymm4, %ymm9
	vmulps	.LC69(%rip), %ymm8, %ymm4
	vminps	%ymm12, %ymm4, %ymm8
	vmaxps	%ymm11, %ymm8, %ymm4
	vmovaps	%ymm4, %ymm11
	vfmadd132ps	%ymm0, %ymm6, %ymm11
	vroundps	$9, %ymm11, %ymm8
	vfmsub132ps	%ymm0, %ymm8, %ymm4
	vmovaps	%ymm4, %ymm11
	vfmadd132ps	%ymm3, %ymm14, %ymm11
	vfmadd132ps	%ymm4, %ymm15, %ymm11
	vfmadd132ps	%ymm4, %ymm13, %ymm11
	vfmadd132ps	%ymm4, %ymm2, %ymm11
	vfmadd132ps	%ymm4, %ymm1, %ymm11
	vcvttps2dq	%ymm8, %ymm4
	vpaddd	%ymm7, %ymm4, %ymm8
	vpslld	$23, %ymm8, %ymm4
	vmulps	.LC71(%rip), %ymm4, %ymm8
	vmulps	%ymm11, %ymm8, %ymm4
	vaddps	.LC73(%rip), %ymm5, %ymm11
	vmulps	.LC75(%rip), %ymm11, %ymm8
	vminps	%ymm12, %ymm8, %ymm12
	vmaxps	864(%rsp), %ymm12, %ymm11
	vmovaps	%ymm11, %ymm12
	vfmadd132ps	%ymm0, %ymm6, %ymm12
	vroundps	$9, %ymm12, %ymm12
	vfmsub132ps	%ymm0, %ymm12, %ymm11
	vmovaps	%ymm11, %ymm8
	vfmadd132ps	%ymm3, %ymm14, %ymm8
	vfmadd132ps	%ymm11, %ymm15, %ymm8
	vfmadd132ps	%ymm11, %ymm13, %ymm8
	vfmadd132ps	%ymm11, %ymm2, %ymm8
	vfmadd132ps	%ymm11, %ymm1, %ymm8
	vcvttps2dq	%ymm12, %ymm11
	vpaddd	%ymm7, %ymm11, %ymm12
	vpslld	$23, %ymm12, %ymm11
	vrcpps	%ymm10, %ymm12
	vfmadd213ps	800(%rsp), %ymm11, %ymm8
	vmulps	%ymm10, %ymm12, %ymm10
	vaddps	%ymm12, %ymm12, %ymm11
	vmulps	%ymm10, %ymm12, %ymm10
	vsubps	%ymm10, %ymm11, %ymm12
	vsubps	0(%r13,%rax), %ymm12, %ymm11
	vmovaps	704(%rsp), %ymm12
	vfmadd213ps	0(%r13,%rax), %ymm12, %ymm11
	vmovups	%ymm11, 0(%r13,%rax)
	vrcpps	%ymm9, %ymm11
	vmulps	%ymm9, %ymm11, %ymm9
	vaddps	%ymm11, %ymm11, %ymm10
	vmulps	%ymm9, %ymm11, %ymm9
	vsubps	%ymm9, %ymm10, %ymm11
	vrcpps	%ymm8, %ymm10
	vsubps	(%rsi,%rax), %ymm11, %ymm9
	vmulps	%ymm12, %ymm9, %ymm11
	vmulps	%ymm8, %ymm10, %ymm8
	vaddps	%ymm10, %ymm10, %ymm12
	vmulps	%ymm8, %ymm10, %ymm9
	vsubps	%ymm9, %ymm12, %ymm10
	vmulps	%ymm10, %ymm4, %ymm4
	vaddps	672(%rsp), %ymm4, %ymm9
	vrcpps	%ymm9, %ymm8
	vmulps	%ymm9, %ymm8, %ymm12
	vaddps	%ymm8, %ymm8, %ymm4
	vmulps	%ymm12, %ymm8, %ymm10
	vaddps	.LC79(%rip), %ymm5, %ymm12
	vsubps	%ymm10, %ymm4, %ymm9
	vmulps	.LC81(%rip), %ymm12, %ymm10
	vmovaps	832(%rsp), %ymm12
	vmulps	%ymm9, %ymm11, %ymm11
	vaddps	(%rsi,%rax), %ymm11, %ymm8
	vmovaps	864(%rsp), %ymm11
	vminps	%ymm12, %ymm10, %ymm4
	vmovups	%ymm8, (%rsi,%rax)
	vmaxps	%ymm11, %ymm4, %ymm8
	vmovaps	%ymm8, %ymm4
	vfmadd132ps	%ymm0, %ymm6, %ymm4
	vroundps	$9, %ymm4, %ymm10
	vfmsub132ps	%ymm0, %ymm10, %ymm8
	vmovaps	%ymm8, %ymm9
	vfmadd132ps	%ymm3, %ymm14, %ymm9
	vfmadd132ps	%ymm8, %ymm15, %ymm9
	vfmadd132ps	%ymm8, %ymm13, %ymm9
	vfmadd132ps	%ymm8, %ymm2, %ymm9
	vfmadd132ps	%ymm8, %ymm1, %ymm9
	vcvttps2dq	%ymm10, %ymm8
	vpaddd	%ymm7, %ymm8, %ymm4
	vpslld	$23, %ymm4, %ymm10
	vfmadd213ps	800(%rsp), %ymm9, %ymm10
	vrcpps	%ymm10, %ymm9
	vmulps	%ymm10, %ymm9, %ymm8
	vaddps	%ymm9, %ymm9, %ymm10
	vmulps	%ymm8, %ymm9, %ymm4
	vaddps	.LC83(%rip), %ymm5, %ymm9
	vsubps	%ymm4, %ymm10, %ymm8
	vmulps	.LC85(%rip), %ymm9, %ymm4
	vminps	%ymm12, %ymm4, %ymm10
	vmaxps	%ymm11, %ymm10, %ymm11
	vmovaps	%ymm11, %ymm10
	vfmadd132ps	%ymm0, %ymm6, %ymm10
	vroundps	$9, %ymm10, %ymm4
	vfmsub132ps	%ymm0, %ymm4, %ymm11
	vmovaps	%ymm11, %ymm9
	vfmadd132ps	%ymm3, %ymm14, %ymm9
	vfmadd132ps	%ymm11, %ymm15, %ymm9
	vfmadd132ps	%ymm11, %ymm13, %ymm9
	vfmadd132ps	%ymm11, %ymm2, %ymm9
	vfmadd132ps	%ymm11, %ymm1, %ymm9
	vcvttps2dq	%ymm4, %ymm11
	vpaddd	%ymm7, %ymm11, %ymm10
	vmovups	(%r12,%rax), %ymm11
	vpslld	$23, %ymm10, %ymm4
	vfmadd213ps	800(%rsp), %ymm4, %ymm9
	vmulps	%ymm8, %ymm8, %ymm10
	vmulps	%ymm8, %ymm10, %ymm8
	vmulps	.LC87(%rip), %ymm8, %ymm4
	vaddps	.LC89(%rip), %ymm5, %ymm8
	vmulps	%ymm11, %ymm4, %ymm10
	vmulps	.LC91(%rip), %ymm8, %ymm4
	vmovaps	%ymm10, 480(%rsp)
	vminps	%ymm12, %ymm4, %ymm12
	vmaxps	864(%rsp), %ymm12, %ymm8
	vmovaps	%ymm8, %ymm10
	vfmadd132ps	%ymm0, %ymm6, %ymm10
	vroundps	$9, %ymm10, %ymm4
	vfmsub132ps	%ymm0, %ymm4, %ymm8
	vcvttps2dq	%ymm4, %ymm4
	vmovaps	%ymm8, %ymm12
	vfmadd132ps	%ymm3, %ymm14, %ymm12
	vfmadd132ps	%ymm8, %ymm15, %ymm12
	vfmadd132ps	%ymm8, %ymm13, %ymm12
	vfmadd132ps	%ymm8, %ymm2, %ymm12
	vfmadd132ps	%ymm8, %ymm1, %ymm12
	vrcpps	%ymm9, %ymm8
	vmulps	%ymm9, %ymm8, %ymm9
	vmulps	%ymm9, %ymm8, %ymm10
	vaddps	%ymm8, %ymm8, %ymm8
	vsubps	%ymm10, %ymm8, %ymm9
	vsubps	%ymm11, %ymm9, %ymm10
	vpaddd	%ymm7, %ymm4, %ymm9
	vmulps	288(%rsp), %ymm10, %ymm8
	vpslld	$23, %ymm9, %ymm10
	vmulps	%ymm10, %ymm12, %ymm12
	vrcpps	%ymm12, %ymm9
	vmulps	%ymm12, %ymm9, %ymm4
	vaddps	%ymm9, %ymm9, %ymm12
	vmulps	%ymm4, %ymm9, %ymm10
	vsubps	%ymm10, %ymm12, %ymm9
	vaddps	.LC93(%rip), %ymm5, %ymm10
	vmulps	%ymm9, %ymm8, %ymm8
	vmulps	.LC95(%rip), %ymm10, %ymm9
	vmovaps	832(%rsp), %ymm10
	vaddps	%ymm11, %ymm8, %ymm11
	vminps	%ymm10, %ymm9, %ymm8
	vmovups	%ymm11, (%r12,%rax)
	vmovups	(%rbx,%rax), %ymm12
	vmulps	%ymm12, %ymm12, %ymm4
	vmulps	%ymm4, %ymm4, %ymm11
	vmaxps	864(%rsp), %ymm8, %ymm4
	vmovaps	%ymm4, %ymm9
	vfmadd132ps	%ymm0, %ymm6, %ymm9
	vroundps	$9, %ymm9, %ymm9
	vfmsub132ps	%ymm0, %ymm9, %ymm4
	vmovaps	%ymm4, %ymm8
	vfmadd132ps	%ymm3, %ymm14, %ymm8
	vfmadd132ps	%ymm4, %ymm15, %ymm8
	vfmadd132ps	%ymm4, %ymm13, %ymm8
	vfmadd132ps	%ymm4, %ymm2, %ymm8
	vfmadd132ps	%ymm4, %ymm1, %ymm8
	vcvttps2dq	%ymm9, %ymm4
	vpaddd	%ymm7, %ymm4, %ymm9
	vpslld	$23, %ymm9, %ymm4
	vaddps	.LC97(%rip), %ymm5, %ymm9
	vfmadd213ps	800(%rsp), %ymm4, %ymm8
	vmulps	.LC99(%rip), %ymm9, %ymm4
	vminps	%ymm10, %ymm4, %ymm10
	vmaxps	864(%rsp), %ymm10, %ymm9
	vmovaps	%ymm9, %ymm10
	vfmadd132ps	%ymm0, %ymm6, %ymm10
	vroundps	$9, %ymm10, %ymm10
	vfmsub132ps	%ymm0, %ymm10, %ymm9
	vmovaps	%ymm9, %ymm4
	vfmadd132ps	%ymm3, %ymm14, %ymm4
	vfmadd132ps	%ymm9, %ymm15, %ymm4
	vfmadd132ps	%ymm9, %ymm13, %ymm4
	vfmadd132ps	%ymm9, %ymm2, %ymm4
	vfmadd132ps	%ymm9, %ymm1, %ymm4
	vcvttps2dq	%ymm10, %ymm9
	vpaddd	%ymm7, %ymm9, %ymm10
	vpslld	$23, %ymm10, %ymm9
	vmulps	.LC101(%rip), %ymm9, %ymm10
	vrcpps	%ymm8, %ymm9
	vfmadd213ps	576(%rsp), %ymm10, %ymm4
	vmulps	%ymm8, %ymm9, %ymm8
	vmulps	%ymm8, %ymm9, %ymm10
	vaddps	%ymm9, %ymm9, %ymm9
	vsubps	%ymm10, %ymm9, %ymm8
	vsubps	%ymm12, %ymm8, %ymm10
	vrcpps	%ymm4, %ymm8
	vmulps	704(%rsp), %ymm10, %ymm9
	vmulps	%ymm4, %ymm8, %ymm4
	vmulps	%ymm4, %ymm8, %ymm10
	vaddps	%ymm8, %ymm8, %ymm8
	vsubps	%ymm10, %ymm8, %ymm4
	vmulps	%ymm4, %ymm9, %ymm9
	vaddps	%ymm12, %ymm9, %ymm12
	vaddps	544(%rsp), %ymm5, %ymm9
	vmovups	%ymm12, (%rbx,%rax)
	vmovups	(%r11,%rax), %ymm12
	vmulps	%ymm12, %ymm12, %ymm10
	vmulps	%ymm10, %ymm10, %ymm8
	vmulps	576(%rsp), %ymm8, %ymm4
	vaddps	.LC111(%rip), %ymm5, %ymm8
	vfmadd231ps	.LC105(%rip), %ymm11, %ymm4
	vaddps	.LC107(%rip), %ymm5, %ymm11
	vmulps	%ymm4, %ymm9, %ymm10
	vmulps	.LC95(%rip), %ymm8, %ymm4
	vfmadd132ps	480(%rsp), %ymm10, %ymm11
	vminps	832(%rsp), %ymm4, %ymm9
	vmulps	.LC113(%rip), %ymm8, %ymm8
	vmaxps	864(%rsp), %ymm9, %ymm9
	vmovaps	%ymm9, %ymm10
	vfmadd132ps	%ymm0, %ymm6, %ymm10
	vroundps	$9, %ymm10, %ymm10
	vfmsub132ps	%ymm0, %ymm10, %ymm9
	vmovaps	%ymm9, %ymm4
	vfmadd132ps	%ymm3, %ymm14, %ymm4
	vfmadd132ps	%ymm9, %ymm15, %ymm4
	vfmadd132ps	%ymm9, %ymm13, %ymm4
	vfmadd132ps	%ymm9, %ymm2, %ymm4
	vfmadd132ps	%ymm9, %ymm1, %ymm4
	vcvttps2dq	%ymm10, %ymm9
	vpaddd	%ymm7, %ymm9, %ymm10
	vpslld	$23, %ymm10, %ymm9
	vfnmadd213ps	800(%rsp), %ymm9, %ymm4
	vrcpps	%ymm4, %ymm10
	vmulps	%ymm4, %ymm10, %ymm4
	vaddps	%ymm10, %ymm10, %ymm9
	vmulps	%ymm4, %ymm10, %ymm4
	vsubps	%ymm4, %ymm9, %ymm10
	vaddps	672(%rsp), %ymm5, %ymm4
	vmulps	.LC115(%rip), %ymm4, %ymm9
	vmulps	%ymm10, %ymm8, %ymm8
	vminps	832(%rsp), %ymm9, %ymm10
	vmaxps	864(%rsp), %ymm10, %ymm9
	vmovaps	%ymm9, %ymm4
	vfmadd132ps	%ymm0, %ymm6, %ymm4
	vroundps	$9, %ymm4, %ymm10
	vfmsub132ps	%ymm0, %ymm10, %ymm9
	vmovaps	%ymm9, %ymm4
	vfmadd132ps	%ymm3, %ymm14, %ymm4
	vfmadd132ps	%ymm9, %ymm15, %ymm4
	vfmadd132ps	%ymm9, %ymm13, %ymm4
	vfmadd132ps	%ymm9, %ymm2, %ymm4
	vfmadd132ps	%ymm9, %ymm1, %ymm4
	vcvttps2dq	%ymm10, %ymm9
	vpaddd	%ymm7, %ymm9, %ymm10
	vpslld	$23, %ymm10, %ymm9
	vmulps	.LC117(%rip), %ymm9, %ymm10
	vfmadd132ps	%ymm10, %ymm8, %ymm4
	vrcpps	%ymm4, %ymm9
	vmulps	%ymm4, %ymm9, %ymm10
	vmulps	%ymm10, %ymm9, %ymm10
	vaddps	%ymm9, %ymm9, %ymm9
	vsubps	%ymm10, %ymm9, %ymm10
	vmulps	%ymm10, %ymm8, %ymm8
	vsubps	%ymm12, %ymm8, %ymm10
	vmovaps	704(%rsp), %ymm8
	vmulps	%ymm8, %ymm4, %ymm4
	vfmadd132ps	%ymm4, %ymm12, %ymm10
	vaddps	448(%rsp), %ymm11, %ymm12
	vmovaps	%ymm8, %ymm11
	vfnmadd132ps	%ymm12, %ymm5, %ymm11
	vmovups	%ymm10, (%r11,%rax)
	vmovaps	%ymm11, 448(%rsp)
	vmovaps	%ymm12, %ymm11
	vmovaps	832(%rsp), %ymm12
	vfmsub132ps	%ymm8, %ymm5, %ymm11
	vmovaps	768(%rsp), %ymm5
	vaddps	.LC79(%rip), %ymm5, %ymm9
	vmulps	.LC81(%rip), %ymm9, %ymm4
	vmovaps	864(%rsp), %ymm9
	vaddps	%ymm5, %ymm11, %ymm10
	vminps	%ymm12, %ymm4, %ymm8
	vmaxps	%ymm9, %ymm8, %ymm5
	vmovaps	%ymm5, %ymm4
	vfmadd132ps	%ymm0, %ymm6, %ymm4
	vroundps	$9, %ymm4, %ymm4
	vfmsub132ps	%ymm0, %ymm4, %ymm5
	vmovaps	%ymm5, %ymm8
	vfmadd132ps	%ymm3, %ymm14, %ymm8
	vfmadd132ps	%ymm5, %ymm15, %ymm8
	vfmadd132ps	%ymm5, %ymm13, %ymm8
	vfmadd132ps	%ymm5, %ymm2, %ymm8
	vfmadd132ps	%ymm5, %ymm1, %ymm8
	vcvttps2dq	%ymm4, %ymm5
	vpaddd	%ymm7, %ymm5, %ymm4
	vpslld	$23, %ymm4, %ymm5
	vfmadd213ps	800(%rsp), %ymm8, %ymm5
	vrcpps	%ymm5, %ymm8
	vmulps	%ymm5, %ymm8, %ymm4
	vmulps	%ymm4, %ymm8, %ymm5
	vaddps	%ymm8, %ymm8, %ymm8
	vmovaps	768(%rsp), %ymm4
	vsubps	%ymm5, %ymm8, %ymm8
	vaddps	.LC119(%rip), %ymm4, %ymm5
	vmulps	.LC85(%rip), %ymm5, %ymm4
	vminps	%ymm12, %ymm4, %ymm12
	vmaxps	%ymm9, %ymm12, %ymm5
	vmovaps	%ymm5, %ymm9
	vfmadd132ps	%ymm0, %ymm6, %ymm9
	vroundps	$9, %ymm9, %ymm12
	vfmsub132ps	%ymm0, %ymm12, %ymm5
	vmovaps	%ymm5, %ymm4
	vfmadd132ps	%ymm3, %ymm14, %ymm4
	vfmadd132ps	%ymm5, %ymm15, %ymm4
	vfmadd132ps	%ymm5, %ymm13, %ymm4
	vfmadd132ps	%ymm5, %ymm2, %ymm4
	vfmadd132ps	%ymm5, %ymm1, %ymm4
	vcvttps2dq	%ymm12, %ymm5
	vpaddd	%ymm7, %ymm5, %ymm9
	vmulps	%ymm8, %ymm8, %ymm5
	vpslld	$23, %ymm9, %ymm12
	vfmadd213ps	800(%rsp), %ymm12, %ymm4
	vmulps	%ymm8, %ymm5, %ymm8
	vmulps	.LC121(%rip), %ymm8, %ymm9
	vmulps	(%r10,%rax), %ymm9, %ymm12
	vmovaps	768(%rsp), %ymm9
	vaddps	.LC107(%rip), %ymm9, %ymm5
	vmulps	%ymm5, %ymm12, %ymm8
	vfmadd132ps	.LC123(%rip), %ymm8, %ymm10
	vmovaps	%ymm10, %ymm12
	vmovaps	%ymm9, %ymm10
	vaddps	.LC89(%rip), %ymm9, %ymm9
	vmulps	.LC91(%rip), %ymm9, %ymm5
	vminps	832(%rsp), %ymm5, %ymm8
	vmaxps	864(%rsp), %ymm8, %ymm9
	vmovaps	%ymm9, %ymm5
	vfmadd132ps	%ymm0, %ymm6, %ymm5
	vroundps	$9, %ymm5, %ymm5
	vfmsub132ps	%ymm0, %ymm5, %ymm9
	vcvttps2dq	%ymm5, %ymm5
	vmovaps	%ymm9, %ymm8
	vfmadd132ps	%ymm3, %ymm14, %ymm8
	vfmadd132ps	%ymm9, %ymm15, %ymm8
	vfmadd132ps	%ymm9, %ymm13, %ymm8
	vfmadd132ps	%ymm9, %ymm2, %ymm8
	vfmadd132ps	%ymm8, %ymm1, %ymm9
	vrcpps	%ymm4, %ymm8
	vmulps	%ymm4, %ymm8, %ymm4
	vmulps	%ymm4, %ymm8, %ymm4
	vaddps	%ymm8, %ymm8, %ymm8
	vsubps	%ymm4, %ymm8, %ymm4
	vsubps	(%r10,%rax), %ymm4, %ymm8
	vmulps	256(%rsp), %ymm8, %ymm8
	vpaddd	%ymm7, %ymm5, %ymm4
	vpslld	$23, %ymm4, %ymm5
	vmulps	%ymm5, %ymm9, %ymm9
	vrcpps	%ymm9, %ymm4
	vmulps	%ymm9, %ymm4, %ymm5
	vmulps	%ymm5, %ymm4, %ymm9
	vaddps	%ymm4, %ymm4, %ymm4
	vsubps	%ymm9, %ymm4, %ymm5
	vmulps	%ymm5, %ymm8, %ymm8
	vaddps	(%r10,%rax), %ymm8, %ymm9
	vmovups	%ymm9, (%r10,%rax)
	vmovups	(%r9,%rax), %ymm4
	vaddps	608(%rsp), %ymm10, %ymm9
	vmulps	%ymm4, %ymm4, %ymm5
	vmulps	%ymm5, %ymm5, %ymm8
	vaddps	544(%rsp), %ymm10, %ymm5
	vaddps	.LC111(%rip), %ymm10, %ymm10
	vmulps	.LC121(%rip), %ymm8, %ymm4
	vmulps	%ymm5, %ymm4, %ymm8
	vmulps	.LC95(%rip), %ymm10, %ymm4
	vfmadd132ps	.LC125(%rip), %ymm8, %ymm9
	vminps	832(%rsp), %ymm4, %ymm5
	vmulps	.LC113(%rip), %ymm10, %ymm10
	vmaxps	864(%rsp), %ymm5, %ymm5
	vmovaps	%ymm5, %ymm8
	vaddps	%ymm12, %ymm9, %ymm12
	vfmadd132ps	%ymm0, %ymm6, %ymm8
	vroundps	$9, %ymm8, %ymm4
	vfmsub132ps	%ymm0, %ymm4, %ymm5
	vmovaps	%ymm5, %ymm8
	vfmadd132ps	%ymm3, %ymm14, %ymm8
	vfmadd132ps	%ymm5, %ymm15, %ymm8
	vfmadd132ps	%ymm5, %ymm13, %ymm8
	vfmadd132ps	%ymm5, %ymm2, %ymm8
	vfmadd132ps	%ymm5, %ymm1, %ymm8
	vcvttps2dq	%ymm4, %ymm5
	vpaddd	%ymm7, %ymm5, %ymm4
	vpslld	$23, %ymm4, %ymm4
	vfnmadd213ps	800(%rsp), %ymm8, %ymm4
	vrcpps	%ymm4, %ymm8
	vmulps	%ymm4, %ymm8, %ymm5
	vmulps	%ymm5, %ymm8, %ymm4
	vaddps	%ymm8, %ymm8, %ymm8
	vsubps	%ymm4, %ymm8, %ymm5
	vmovaps	768(%rsp), %ymm4
	vaddps	672(%rsp), %ymm4, %ymm8
	vmulps	%ymm5, %ymm10, %ymm10
	vmulps	.LC115(%rip), %ymm8, %ymm5
	vminps	832(%rsp), %ymm5, %ymm4
	vmaxps	864(%rsp), %ymm4, %ymm8
	vfmadd231ps	%ymm0, %ymm8, %ymm6
	vroundps	$9, %ymm6, %ymm6
	vfmsub132ps	%ymm0, %ymm6, %ymm8
	vfmadd132ps	%ymm8, %ymm14, %ymm3
	vfmadd132ps	%ymm8, %ymm15, %ymm3
	vfmadd132ps	%ymm8, %ymm13, %ymm3
	vfmadd132ps	%ymm8, %ymm2, %ymm3
	vfmadd132ps	%ymm8, %ymm1, %ymm3
	vcvttps2dq	%ymm6, %ymm1
	vpaddd	%ymm7, %ymm1, %ymm0
	vpslld	$23, %ymm0, %ymm13
	vmulps	.LC117(%rip), %ymm13, %ymm14
	vmovaps	.LC32(%rip), %ymm0
	vmovaps	704(%rsp), %ymm1
	vmovaps	768(%rsp), %ymm9
	vmovaps	%ymm0, 480(%rsp)
	vfnmadd231ps	%ymm1, %ymm12, %ymm9
	vmovaps	640(%rsp), %ymm12
	vfmadd132ps	%ymm14, %ymm10, %ymm3
	vaddps	%ymm0, %ymm12, %ymm13
	vaddps	%ymm12, %ymm11, %ymm11
	vmovaps	.LC44(%rip), %ymm0
	vmulps	.LC127(%rip), %ymm13, %ymm14
	vbroadcastss	.LC45(%rip), %ymm13
	vmovaps	%ymm9, 768(%rsp)
	vmovaps	%ymm11, 416(%rsp)
	vrcpps	%ymm3, %ymm15
	vmulps	%ymm3, %ymm15, %ymm2
	vaddps	%ymm15, %ymm15, %ymm4
	vmulps	%ymm1, %ymm3, %ymm3
	vmulps	%ymm2, %ymm15, %ymm5
	vsubps	%ymm5, %ymm4, %ymm8
	vmovaps	.LC103(%rip), %ymm5
	vbroadcastss	.LC104(%rip), %ymm4
	vmovaps	%ymm5, 576(%rsp)
	vmulps	%ymm8, %ymm10, %ymm10
	vsubps	%ymm12, %ymm4, %ymm8
	vbroadcastss	.LC49(%rip), %ymm4
	vsubps	(%r9,%rax), %ymm10, %ymm6
	vfmadd213ps	(%r9,%rax), %ymm3, %ymm6
	vmulps	.LC129(%rip), %ymm8, %ymm10
	vmovaps	.LC42(%rip), %ymm3
	vmovaps	%ymm3, 864(%rsp)
	vmovups	%ymm6, (%r9,%rax)
	vmovaps	.LC40(%rip), %ymm6
	vmovups	(%r8,%rax), %ymm11
	vminps	%ymm6, %ymm10, %ymm1
	vmulps	%ymm11, %ymm11, %ymm15
	vmovaps	%ymm6, 832(%rsp)
	vmovaps	.LC46(%rip), %ymm6
	vmaxps	%ymm3, %ymm1, %ymm9
	vmovaps	.LC48(%rip), %ymm3
	vbroadcastss	.LC59(%rip), %ymm1
	vmulps	%ymm15, %ymm14, %ymm2
	vmovaps	.LC50(%rip), %ymm14
	vmovaps	.LC52(%rip), %ymm15
	vfmadd132ps	%ymm9, %ymm6, %ymm13
	vmovaps	%ymm2, 384(%rsp)
	vbroadcastss	.LC57(%rip), %ymm2
	vroundps	$9, %ymm13, %ymm5
	vfmsub132ps	%ymm0, %ymm5, %ymm9
	vcvttps2dq	%ymm5, %ymm8
	vbroadcastss	.LC55(%rip), %ymm13
	vpaddd	%ymm7, %ymm8, %ymm10
	vpslld	$23, %ymm10, %ymm5
	vfmadd132ps	%ymm9, %ymm14, %ymm4
	vfmadd132ps	%ymm9, %ymm15, %ymm4
	vfmadd132ps	%ymm9, %ymm13, %ymm4
	vfmadd132ps	%ymm9, %ymm2, %ymm4
	vfmadd132ps	%ymm4, %ymm1, %ymm9
	vbroadcastss	.LC62(%rip), %ymm4
	movq	320(%rsp), %rdi
	vmovaps	%ymm4, 800(%rsp)
	vfmadd132ps	%ymm9, %ymm4, %ymm5
	vrcpps	%ymm5, %ymm9
	vmulps	%ymm5, %ymm9, %ymm8
	vaddps	%ymm9, %ymm9, %ymm5
	vmulps	%ymm8, %ymm9, %ymm10
	vaddps	.LC133(%rip), %ymm12, %ymm8
	vmulps	.LC135(%rip), %ymm8, %ymm9
	vmulps	.LC138(%rip), %ymm8, %ymm8
	vsubps	%ymm10, %ymm5, %ymm4
	vminps	.LC40(%rip), %ymm9, %ymm10
	vbroadcastss	.LC49(%rip), %ymm5
	vmaxps	.LC42(%rip), %ymm10, %ymm9
	vmulps	.LC131(%rip), %ymm4, %ymm4
	vbroadcastss	.LC45(%rip), %ymm10
	vfmadd132ps	%ymm9, %ymm6, %ymm10
	vroundps	$9, %ymm10, %ymm10
	vfmsub132ps	%ymm0, %ymm10, %ymm9
	vfmadd132ps	%ymm9, %ymm14, %ymm5
	vfmadd132ps	%ymm9, %ymm15, %ymm5
	vfmadd132ps	%ymm9, %ymm13, %ymm5
	vfmadd132ps	%ymm9, %ymm2, %ymm5
	vfmadd132ps	%ymm9, %ymm1, %ymm5
	vcvttps2dq	%ymm10, %ymm9
	vpaddd	%ymm7, %ymm9, %ymm10
	vpslld	$23, %ymm10, %ymm9
	vfmadd213ps	.LC136(%rip), %ymm9, %ymm5
	vrcpps	%ymm5, %ymm10
	vmulps	%ymm5, %ymm10, %ymm5
	vaddps	%ymm10, %ymm10, %ymm9
	vmulps	%ymm5, %ymm10, %ymm5
	vsubps	%ymm5, %ymm9, %ymm10
	vmulps	%ymm10, %ymm8, %ymm8
	vaddps	%ymm4, %ymm8, %ymm10
	vrcpps	%ymm10, %ymm5
	vmulps	%ymm10, %ymm5, %ymm9
	vmulps	224(%rsp), %ymm10, %ymm10
	vmulps	%ymm9, %ymm5, %ymm8
	vaddps	%ymm5, %ymm5, %ymm5
	vsubps	%ymm8, %ymm5, %ymm9
	vbroadcastss	.LC31(%rip), %ymm8
	vmovaps	%ymm8, 608(%rsp)
	vmulps	%ymm9, %ymm4, %ymm4
	vbroadcastss	.LC110(%rip), %ymm9
	vmovaps	%ymm9, 544(%rsp)
	vsubps	%ymm11, %ymm4, %ymm5
	vfmadd132ps	%ymm10, %ymm11, %ymm5
	vmovaps	%ymm12, %ymm11
	vaddps	%ymm12, %ymm8, %ymm12
	vaddps	%ymm11, %ymm9, %ymm4
	vmovups	%ymm5, (%r8,%rax)
	vmovups	(%rdi,%rax), %ymm10
	vbroadcastss	.LC78(%rip), %ymm5
	vmovaps	%ymm5, 672(%rsp)
	vmulps	%ymm5, %ymm10, %ymm8
	vmulps	%ymm8, %ymm4, %ymm9
	vmovups	(%rcx,%rax), %ymm4
	vmulps	.LC142(%rip), %ymm4, %ymm5
	vfmadd132ps	.LC140(%rip), %ymm9, %ymm12
	vminps	.LC144(%rip), %ymm5, %ymm4
	vaddps	.LC146(%rip), %ymm4, %ymm8
	vrcpps	%ymm8, %ymm5
	vmulps	%ymm8, %ymm5, %ymm9
	vmulps	704(%rsp), %ymm8, %ymm8
	vmulps	%ymm9, %ymm5, %ymm9
	vaddps	%ymm5, %ymm5, %ymm5
	vsubps	%ymm9, %ymm5, %ymm9
	vmulps	%ymm9, %ymm4, %ymm4
	vsubps	%ymm10, %ymm4, %ymm5
	vfmadd132ps	%ymm8, %ymm10, %ymm5
	vaddps	.LC148(%rip), %ymm11, %ymm10
	vmovups	%ymm5, (%rdi,%rax)
	vmovups	(%rdx,%rax), %ymm9
	vmulps	.LC150(%rip), %ymm9, %ymm4
	vfmadd213ps	128(%rsp), %ymm4, %ymm10
	vaddps	.LC152(%rip), %ymm11, %ymm5
	vmulps	.LC154(%rip), %ymm5, %ymm8
	vbroadcastss	.LC45(%rip), %ymm4
	vaddps	%ymm10, %ymm12, %ymm12
	vminps	.LC40(%rip), %ymm8, %ymm10
	vmaxps	.LC42(%rip), %ymm10, %ymm9
	vfmadd132ps	%ymm9, %ymm6, %ymm4
	vroundps	$9, %ymm4, %ymm5
	vfmsub132ps	%ymm0, %ymm5, %ymm9
	vcvttps2dq	%ymm5, %ymm8
	vbroadcastss	.LC49(%rip), %ymm4
	vbroadcastss	.LC157(%rip), %ymm5
	vpaddd	%ymm7, %ymm8, %ymm10
	vfmadd213ps	.LC158(%rip), %ymm11, %ymm5
	vminps	.LC40(%rip), %ymm5, %ymm8
	vmaxps	.LC42(%rip), %ymm8, %ymm8
	vbroadcastss	.LC161(%rip), %ymm5
	vfmadd213ps	.LC162(%rip), %ymm11, %ymm5
	vmovaps	.LC40(%rip), %ymm11
	vfmadd132ps	%ymm9, %ymm14, %ymm4
	vfmadd132ps	%ymm9, %ymm15, %ymm4
	vfmadd132ps	%ymm9, %ymm13, %ymm4
	vfmadd132ps	%ymm9, %ymm2, %ymm4
	vfmadd132ps	%ymm9, %ymm1, %ymm4
	vpslld	$23, %ymm10, %ymm9
	vbroadcastss	.LC45(%rip), %ymm10
	vfmadd213ps	800(%rsp), %ymm9, %ymm4
	vbroadcastss	.LC49(%rip), %ymm9
	vfmadd132ps	%ymm8, %ymm6, %ymm10
	vroundps	$9, %ymm10, %ymm10
	vfmsub132ps	%ymm0, %ymm10, %ymm8
	vcvttps2dq	%ymm10, %ymm10
	vfmadd132ps	%ymm8, %ymm14, %ymm9
	vfmadd132ps	%ymm8, %ymm15, %ymm9
	vfmadd132ps	%ymm8, %ymm13, %ymm9
	vfmadd132ps	%ymm8, %ymm2, %ymm9
	vfmadd132ps	%ymm9, %ymm1, %ymm8
	vminps	%ymm5, %ymm11, %ymm9
	vmaxps	.LC42(%rip), %ymm9, %ymm9
	vbroadcastss	.LC45(%rip), %ymm11
	vbroadcastss	.LC49(%rip), %ymm5
	vfmadd132ps	%ymm9, %ymm6, %ymm11
	vroundps	$9, %ymm11, %ymm11
	vfmsub132ps	%ymm0, %ymm11, %ymm9
	vcvttps2dq	%ymm11, %ymm11
	vfmadd132ps	%ymm9, %ymm14, %ymm5
	vfmadd132ps	%ymm9, %ymm15, %ymm5
	vfmadd132ps	%ymm9, %ymm13, %ymm5
	vfmadd132ps	%ymm9, %ymm2, %ymm5
	vfmadd132ps	%ymm9, %ymm1, %ymm5
	vpaddd	%ymm7, %ymm10, %ymm9
	vpslld	$23, %ymm9, %ymm10
	vpaddd	%ymm7, %ymm11, %ymm9
	vpslld	$23, %ymm9, %ymm11
	vmulps	%ymm11, %ymm5, %ymm5
	vfmadd231ps	%ymm10, %ymm8, %ymm5
	vrcpps	%ymm4, %ymm8
	vmulps	%ymm4, %ymm8, %ymm4
	vaddps	%ymm8, %ymm8, %ymm9
	vmulps	%ymm4, %ymm8, %ymm10
	vmovaps	192(%rsp), %ymm4
	vsubps	%ymm10, %ymm9, %ymm11
	vsubps	(%rdx,%rax), %ymm11, %ymm8
	vmovaps	704(%rsp), %ymm9
	vmovaps	640(%rsp), %ymm11
	vfmsub213ps	160(%rsp), %ymm11, %ymm4
	vmovaps	384(%rsp), %ymm10
	vmulps	%ymm9, %ymm5, %ymm5
	vfmadd132ps	.LC164(%rip), %ymm10, %ymm4
	vfmadd213ps	(%rdx,%rax), %ymm5, %ymm8
	vmovups	%ymm8, (%rdx,%rax)
	vmovups	(%rcx,%rax), %ymm5
	vmovaps	416(%rsp), %ymm8
	vfmadd231ps	.LC166(%rip), %ymm8, %ymm4
	vmulps	.LC168(%rip), %ymm5, %ymm8
	vfmsub231ps	.LC170(%rip), %ymm10, %ymm8
	movq	528(%rsp), %rdi
	vfmadd213ps	(%rcx,%rax), %ymm9, %ymm8
	vaddps	%ymm4, %ymm12, %ymm12
	vfnmadd132ps	%ymm9, %ymm11, %ymm12
	vmovups	%ymm8, (%rcx,%rax)
	vmovaps	448(%rsp), %ymm9
	vmovaps	768(%rsp), %ymm11
	vmovups	%ymm9, (%r15,%rax)
	vmovups	%ymm11, (%r14,%rax)
	vmovups	%ymm12, (%rdi,%rax)
	addq	$32, %rax
	cmpq	%rax, 328(%rsp)
	jne	.L28
	movl	8(%rsp), %r14d
	movq	(%rsp), %r15
	movl	%r14d, %edx
	andl	$-8, %edx
	addl	%edx, 524(%rsp)
	cmpl	%r14d, %edx
	je	.L103
	vzeroupper
.L27:
	subl	%edx, %r14d
	leal	-1(%r14), %r13d
	movl	%r14d, 544(%rsp)
	cmpl	$2, %r13d
	jbe	.L32
	movslq	512(%rsp), %rsi
	movslq	736(%rsp), %rax
	movq	48(%rsp), %r9
	movq	536(%rsp), %rbx
	addq	%rsi, %rax
	movq	32(%rsp), %rsi
	movq	752(%rsp), %r11
	addq	%rdx, %rax
	movq	40(%rsp), %rcx
	movq	56(%rsp), %r8
	salq	$2, %rax
	movq	744(%rsp), %r12
	movq	64(%rsp), %rdx
	addq	%rax, %rsi
	leaq	(%r9,%rax), %r14
	movq	88(%rsp), %r9
	addq	%rax, %rbx
	vmovups	(%rsi), %xmm1
	leaq	(%r11,%rax), %r10
	addq	%rax, %rcx
	leaq	(%r12,%rax), %rdi
	addq	%rax, %r9
	vmovups	(%r10), %xmm0
	vmovups	(%rdi), %xmm11
	leaq	(%r8,%rax), %r13
	vmulps	%xmm1, %xmm1, %xmm4
	movq	%rbx, 704(%rsp)
	vaddps	.LC175(%rip), %xmm11, %xmm12
	leaq	(%rdx,%rax), %r12
	movq	%r9, 608(%rsp)
	movq	704(%rsp), %r9
	vsubps	%xmm0, %xmm11, %xmm14
	leaq	(%r15,%rax), %rdx
	vbroadcastss	.LC27(%rip), %xmm3
	movq	72(%rsp), %rbx
	vmovaps	%xmm0, 800(%rsp)
	vmovups	(%r9), %xmm7
	movq	%r10, %r9
	movq	360(%rsp), %r10
	movq	352(%rsp), %r8
	movq	80(%rsp), %r11
	leaq	(%rbx,%rax), %rbx
	vmulps	%xmm1, %xmm4, %xmm10
	vsubps	%xmm7, %xmm11, %xmm6
	vaddps	.LC174(%rip), %xmm11, %xmm2
	vbroadcastss	.LC29(%rip), %xmm13
	vmulps	(%rcx), %xmm10, %xmm5
	addq	%rax, %r8
	leaq	(%r11,%rax), %r11
	vmovaps	%xmm7, 832(%rsp)
	vmulps	(%r10,%rax), %xmm5, %xmm8
	movq	%r8, 576(%rsp)
	vmulps	%xmm3, %xmm6, %xmm15
	movq	96(%rsp), %r8
	vbroadcastss	.LC35(%rip), %xmm7
	vbroadcastss	.LC39(%rip), %xmm3
	vbroadcastss	.LC41(%rip), %xmm10
	vbroadcastss	.LC57(%rip), %xmm5
	addq	%rax, %r8
	movl	$127, %eax
	vmulps	%xmm12, %xmm8, %xmm9
	vbroadcastss	.LC51(%rip), %xmm8
	vfmadd132ps	%xmm13, %xmm15, %xmm14
	vfmadd132ps	%xmm7, %xmm9, %xmm2
	vbroadcastss	.LC43(%rip), %xmm9
	vbroadcastss	.LC53(%rip), %xmm7
	vaddps	%xmm2, %xmm14, %xmm0
	vbroadcastss	.LC37(%rip), %xmm14
	vbroadcastss	.LC47(%rip), %xmm2
	vaddps	%xmm14, %xmm11, %xmm6
	vmovaps	%xmm0, 672(%rsp)
	vbroadcastss	.LC45(%rip), %xmm0
	vmulps	%xmm3, %xmm6, %xmm15
	vbroadcastss	.LC55(%rip), %xmm6
	vminps	%xmm10, %xmm15, %xmm13
	vmovd	%eax, %xmm15
	vpshufd	$0, %xmm15, %xmm15
	vmovdqa	%xmm15, 864(%rsp)
	vmaxps	%xmm9, %xmm13, %xmm4
	vmovaps	%xmm4, %xmm1
	vfmadd132ps	%xmm0, %xmm2, %xmm1
	vroundps	$9, %xmm1, %xmm14
	vfmsub132ps	%xmm0, %xmm14, %xmm4
	vcvttps2dq	%xmm14, %xmm3
	vbroadcastss	.LC49(%rip), %xmm1
	vpaddd	%xmm15, %xmm3, %xmm13
	vpslld	$23, %xmm13, %xmm14
	vbroadcastss	.LC66(%rip), %xmm13
	vmovaps	%xmm4, %xmm12
	vfmadd132ps	%xmm1, %xmm8, %xmm12
	vfmadd132ps	%xmm4, %xmm7, %xmm12
	vfmadd132ps	%xmm4, %xmm6, %xmm12
	vfmadd132ps	%xmm4, %xmm5, %xmm12
	vfmadd213ps	.LC188(%rip), %xmm12, %xmm4
	vbroadcastss	.LC64(%rip), %xmm12
	vfmadd213ps	.LC190(%rip), %xmm14, %xmm4
	vaddps	%xmm12, %xmm11, %xmm3
	vmulps	%xmm13, %xmm3, %xmm14
	vminps	%xmm10, %xmm14, %xmm12
	vmaxps	%xmm9, %xmm12, %xmm3
	vmovaps	%xmm3, %xmm13
	vfmadd132ps	%xmm0, %xmm2, %xmm13
	vroundps	$9, %xmm13, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm3
	vcvttps2dq	%xmm12, %xmm14
	vmovaps	%xmm3, %xmm13
	vfmadd132ps	%xmm1, %xmm8, %xmm13
	vfmadd132ps	%xmm3, %xmm7, %xmm13
	vfmadd132ps	%xmm3, %xmm6, %xmm13
	vfmadd132ps	%xmm3, %xmm5, %xmm13
	vfmadd213ps	.LC188(%rip), %xmm3, %xmm13
	vpaddd	%xmm15, %xmm14, %xmm3
	vbroadcastss	.LC68(%rip), %xmm14
	vpslld	$23, %xmm3, %xmm12
	vfmadd213ps	.LC190(%rip), %xmm12, %xmm13
	vbroadcastss	.LC70(%rip), %xmm12
	vaddps	%xmm14, %xmm11, %xmm3
	vmulps	%xmm12, %xmm3, %xmm14
	vminps	%xmm10, %xmm14, %xmm3
	vmaxps	%xmm9, %xmm3, %xmm3
	vmovaps	%xmm3, %xmm12
	vfmadd132ps	%xmm0, %xmm2, %xmm12
	vroundps	$9, %xmm12, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm3
	vmovaps	%xmm3, %xmm14
	vfmadd132ps	%xmm1, %xmm8, %xmm14
	vfmadd132ps	%xmm3, %xmm7, %xmm14
	vfmadd132ps	%xmm3, %xmm6, %xmm14
	vfmadd132ps	%xmm3, %xmm5, %xmm14
	vfmadd213ps	.LC188(%rip), %xmm3, %xmm14
	vcvttps2dq	%xmm12, %xmm3
	vbroadcastss	.LC72(%rip), %xmm12
	vpaddd	%xmm15, %xmm3, %xmm15
	vpslld	$23, %xmm15, %xmm3
	vmulps	%xmm12, %xmm3, %xmm15
	vbroadcastss	.LC76(%rip), %xmm12
	vmulps	%xmm14, %xmm15, %xmm3
	vbroadcastss	.LC74(%rip), %xmm14
	vaddps	%xmm14, %xmm11, %xmm15
	vmulps	%xmm12, %xmm15, %xmm14
	vminps	%xmm10, %xmm14, %xmm15
	vmaxps	%xmm9, %xmm15, %xmm14
	vmovaps	%xmm14, %xmm15
	vfmadd132ps	%xmm0, %xmm2, %xmm15
	vroundps	$9, %xmm15, %xmm15
	vfmsub132ps	%xmm0, %xmm15, %xmm14
	vmovaps	%xmm14, %xmm12
	vfmadd132ps	%xmm1, %xmm8, %xmm12
	vfmadd132ps	%xmm14, %xmm7, %xmm12
	vfmadd132ps	%xmm14, %xmm6, %xmm12
	vfmadd132ps	%xmm14, %xmm5, %xmm12
	vfmadd213ps	.LC188(%rip), %xmm14, %xmm12
	vcvttps2dq	%xmm15, %xmm14
	vpaddd	864(%rsp), %xmm14, %xmm15
	vpslld	$23, %xmm15, %xmm14
	vrcpps	%xmm4, %xmm15
	vfmadd213ps	.LC190(%rip), %xmm14, %xmm12
	vmulps	%xmm4, %xmm15, %xmm4
	vaddps	%xmm15, %xmm15, %xmm14
	vmulps	%xmm4, %xmm15, %xmm4
	vsubps	%xmm4, %xmm14, %xmm15
	vsubps	(%rsi), %xmm15, %xmm14
	vbroadcastss	764(%rsp), %xmm4
	vfmadd213ps	(%rsi), %xmm4, %xmm14
	vmovaps	%xmm4, %xmm15
	vmovups	%xmm14, (%rsi)
	vrcpps	%xmm13, %xmm14
	vmovaps	%xmm15, 768(%rsp)
	vmulps	%xmm13, %xmm14, %xmm13
	vaddps	%xmm14, %xmm14, %xmm4
	vmulps	%xmm13, %xmm14, %xmm13
	vsubps	%xmm13, %xmm4, %xmm14
	vrcpps	%xmm12, %xmm13
	vsubps	(%rcx), %xmm14, %xmm4
	vmulps	%xmm15, %xmm4, %xmm14
	vmulps	%xmm12, %xmm13, %xmm12
	vaddps	%xmm13, %xmm13, %xmm15
	vmulps	%xmm12, %xmm13, %xmm4
	vsubps	%xmm4, %xmm15, %xmm13
	vmulps	%xmm13, %xmm3, %xmm3
	vaddps	.LC198(%rip), %xmm3, %xmm4
	vrcpps	%xmm4, %xmm12
	vmulps	%xmm4, %xmm12, %xmm15
	vaddps	%xmm12, %xmm12, %xmm3
	vmulps	%xmm15, %xmm12, %xmm13
	vaddps	.LC199(%rip), %xmm11, %xmm15
	vsubps	%xmm13, %xmm3, %xmm4
	vmulps	.LC200(%rip), %xmm15, %xmm13
	vmulps	%xmm4, %xmm14, %xmm14
	vaddps	(%rcx), %xmm14, %xmm12
	vminps	%xmm10, %xmm13, %xmm3
	vmovups	%xmm12, (%rcx)
	vmaxps	%xmm9, %xmm3, %xmm4
	vmovaps	%xmm4, %xmm14
	vfmadd132ps	%xmm0, %xmm2, %xmm14
	vroundps	$9, %xmm14, %xmm15
	vfmsub132ps	%xmm0, %xmm15, %xmm4
	vcvttps2dq	%xmm15, %xmm13
	vmovdqa	864(%rsp), %xmm15
	vpaddd	%xmm15, %xmm13, %xmm3
	vpslld	$23, %xmm3, %xmm14
	vmovaps	%xmm4, %xmm12
	vfmadd132ps	%xmm1, %xmm8, %xmm12
	vfmadd132ps	%xmm4, %xmm7, %xmm12
	vfmadd132ps	%xmm4, %xmm6, %xmm12
	vfmadd132ps	%xmm4, %xmm5, %xmm12
	vfmadd213ps	.LC188(%rip), %xmm4, %xmm12
	vfmadd213ps	.LC190(%rip), %xmm12, %xmm14
	vrcpps	%xmm14, %xmm4
	vmulps	%xmm14, %xmm4, %xmm12
	vaddps	%xmm4, %xmm4, %xmm3
	vbroadcastss	.LC84(%rip), %xmm14
	vmulps	%xmm12, %xmm4, %xmm13
	vaddps	%xmm14, %xmm11, %xmm12
	vsubps	%xmm13, %xmm3, %xmm4
	vmulps	.LC202(%rip), %xmm12, %xmm13
	vminps	%xmm10, %xmm13, %xmm3
	vmaxps	%xmm9, %xmm3, %xmm3
	vmovaps	%xmm3, %xmm13
	vfmadd132ps	%xmm0, %xmm2, %xmm13
	vroundps	$9, %xmm13, %xmm14
	vfmsub132ps	%xmm0, %xmm14, %xmm3
	vmovaps	%xmm3, %xmm12
	vfmadd132ps	%xmm1, %xmm8, %xmm12
	vfmadd132ps	%xmm3, %xmm7, %xmm12
	vfmadd132ps	%xmm3, %xmm6, %xmm12
	vfmadd132ps	%xmm3, %xmm5, %xmm12
	vfmadd213ps	.LC188(%rip), %xmm3, %xmm12
	vcvttps2dq	%xmm14, %xmm3
	vpaddd	%xmm15, %xmm3, %xmm13
	vmulps	%xmm4, %xmm4, %xmm3
	vpslld	$23, %xmm13, %xmm14
	vfmadd213ps	.LC190(%rip), %xmm14, %xmm12
	vmovups	(%r14), %xmm14
	vmulps	%xmm4, %xmm3, %xmm13
	vbroadcastss	.LC88(%rip), %xmm4
	vmulps	%xmm4, %xmm13, %xmm3
	vaddps	.LC204(%rip), %xmm11, %xmm4
	vmulps	%xmm14, %xmm3, %xmm13
	vmulps	.LC205(%rip), %xmm4, %xmm3
	vmovaps	%xmm13, 640(%rsp)
	vminps	%xmm10, %xmm3, %xmm13
	vmaxps	%xmm9, %xmm13, %xmm4
	vmovaps	%xmm4, %xmm3
	vfmadd132ps	%xmm0, %xmm2, %xmm3
	vroundps	$9, %xmm3, %xmm3
	vfmsub132ps	%xmm0, %xmm3, %xmm4
	vcvttps2dq	%xmm3, %xmm3
	vmovaps	%xmm4, %xmm13
	vfmadd132ps	%xmm1, %xmm8, %xmm13
	vfmadd132ps	%xmm4, %xmm7, %xmm13
	vfmadd132ps	%xmm4, %xmm6, %xmm13
	vfmadd132ps	%xmm4, %xmm5, %xmm13
	vfmadd213ps	.LC188(%rip), %xmm13, %xmm4
	vrcpps	%xmm12, %xmm13
	vmulps	%xmm12, %xmm13, %xmm12
	vmulps	%xmm12, %xmm13, %xmm12
	vaddps	%xmm13, %xmm13, %xmm13
	vsubps	%xmm12, %xmm13, %xmm12
	vsubps	%xmm14, %xmm12, %xmm13
	vbroadcastss	344(%rsp), %xmm12
	vmulps	%xmm12, %xmm13, %xmm12
	vmovdqa	%xmm15, %xmm13
	vpaddd	%xmm15, %xmm3, %xmm15
	vpslld	$23, %xmm15, %xmm3
	vmulps	%xmm3, %xmm4, %xmm15
	vrcpps	%xmm15, %xmm4
	vmulps	%xmm15, %xmm4, %xmm3
	vmulps	%xmm3, %xmm4, %xmm15
	vaddps	%xmm4, %xmm4, %xmm4
	vsubps	%xmm15, %xmm4, %xmm3
	vmulps	%xmm3, %xmm12, %xmm12
	vbroadcastss	.LC94(%rip), %xmm3
	vaddps	%xmm14, %xmm12, %xmm14
	vaddps	%xmm3, %xmm11, %xmm12
	vmovups	%xmm14, (%r14)
	vmovups	0(%r13), %xmm15
	vmulps	%xmm15, %xmm15, %xmm4
	vmulps	%xmm4, %xmm4, %xmm14
	vmulps	.LC207(%rip), %xmm12, %xmm4
	vminps	%xmm10, %xmm4, %xmm3
	vmaxps	%xmm9, %xmm3, %xmm3
	vmovaps	%xmm3, %xmm12
	vfmadd132ps	%xmm0, %xmm2, %xmm12
	vroundps	$9, %xmm12, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm3
	vmovaps	%xmm3, %xmm4
	vfmadd132ps	%xmm1, %xmm8, %xmm4
	vfmadd132ps	%xmm3, %xmm7, %xmm4
	vfmadd132ps	%xmm3, %xmm6, %xmm4
	vfmadd132ps	%xmm3, %xmm5, %xmm4
	vfmadd213ps	.LC188(%rip), %xmm3, %xmm4
	vcvttps2dq	%xmm12, %xmm3
	vpaddd	%xmm13, %xmm3, %xmm13
	vbroadcastss	.LC98(%rip), %xmm3
	vpslld	$23, %xmm13, %xmm12
	vfmadd213ps	.LC190(%rip), %xmm12, %xmm4
	vbroadcastss	.LC100(%rip), %xmm12
	vaddps	%xmm3, %xmm11, %xmm13
	vmulps	%xmm12, %xmm13, %xmm3
	vminps	%xmm10, %xmm3, %xmm13
	vmaxps	%xmm9, %xmm13, %xmm12
	vmovaps	%xmm12, %xmm3
	vfmadd132ps	%xmm0, %xmm2, %xmm3
	vroundps	$9, %xmm3, %xmm3
	vfmsub132ps	%xmm0, %xmm3, %xmm12
	vcvttps2dq	%xmm3, %xmm3
	vmovaps	%xmm12, %xmm13
	vfmadd132ps	%xmm1, %xmm8, %xmm13
	vfmadd132ps	%xmm12, %xmm7, %xmm13
	vfmadd132ps	%xmm12, %xmm6, %xmm13
	vfmadd132ps	%xmm12, %xmm5, %xmm13
	vfmadd213ps	.LC188(%rip), %xmm13, %xmm12
	vpaddd	864(%rsp), %xmm3, %xmm13
	vpslld	$23, %xmm13, %xmm3
	vbroadcastss	.LC102(%rip), %xmm13
	vmulps	%xmm13, %xmm3, %xmm3
	vfmadd213ps	.LC211(%rip), %xmm12, %xmm3
	vrcpps	%xmm4, %xmm12
	vmulps	%xmm4, %xmm12, %xmm4
	vmulps	%xmm4, %xmm12, %xmm13
	vaddps	%xmm12, %xmm12, %xmm12
	vsubps	%xmm13, %xmm12, %xmm4
	vrcpps	%xmm3, %xmm12
	vsubps	%xmm15, %xmm4, %xmm13
	vmulps	768(%rsp), %xmm13, %xmm4
	vmulps	%xmm3, %xmm12, %xmm3
	vmulps	%xmm3, %xmm12, %xmm13
	vaddps	%xmm12, %xmm12, %xmm12
	vsubps	%xmm13, %xmm12, %xmm3
	vmulps	%xmm3, %xmm4, %xmm4
	vaddps	%xmm15, %xmm4, %xmm15
	vbroadcastss	.LC106(%rip), %xmm4
	vmovups	%xmm15, 0(%r13)
	vmovups	(%r12), %xmm13
	vmulps	%xmm13, %xmm13, %xmm12
	vaddps	.LC214(%rip), %xmm11, %xmm13
	vmulps	%xmm12, %xmm12, %xmm3
	vmulps	.LC211(%rip), %xmm3, %xmm15
	vfmadd132ps	%xmm14, %xmm15, %xmm4
	vbroadcastss	.LC108(%rip), %xmm15
	vaddps	%xmm15, %xmm11, %xmm14
	vmulps	%xmm4, %xmm13, %xmm12
	vaddps	.LC215(%rip), %xmm11, %xmm4
	vmulps	.LC207(%rip), %xmm4, %xmm3
	vfmadd132ps	640(%rsp), %xmm12, %xmm14
	vmulps	.LC216(%rip), %xmm4, %xmm4
	vminps	%xmm10, %xmm3, %xmm13
	vmaxps	%xmm9, %xmm13, %xmm12
	vmovaps	%xmm12, %xmm13
	vfmadd132ps	%xmm0, %xmm2, %xmm13
	vroundps	$9, %xmm13, %xmm13
	vfmsub132ps	%xmm0, %xmm13, %xmm12
	vmovaps	%xmm12, %xmm3
	vfmadd132ps	%xmm1, %xmm8, %xmm3
	vfmadd132ps	%xmm12, %xmm7, %xmm3
	vfmadd132ps	%xmm12, %xmm6, %xmm3
	vfmadd132ps	%xmm12, %xmm5, %xmm3
	vfmadd213ps	.LC188(%rip), %xmm12, %xmm3
	vcvttps2dq	%xmm13, %xmm12
	vpaddd	864(%rsp), %xmm12, %xmm13
	vpslld	$23, %xmm13, %xmm12
	vfnmadd213ps	.LC190(%rip), %xmm12, %xmm3
	vrcpps	%xmm3, %xmm13
	vmulps	%xmm3, %xmm13, %xmm3
	vaddps	%xmm13, %xmm13, %xmm12
	vmulps	%xmm3, %xmm13, %xmm3
	vsubps	%xmm3, %xmm12, %xmm13
	vaddps	.LC198(%rip), %xmm11, %xmm3
	vmulps	.LC217(%rip), %xmm3, %xmm12
	vmulps	%xmm13, %xmm4, %xmm4
	vminps	%xmm10, %xmm12, %xmm13
	vmaxps	%xmm9, %xmm13, %xmm12
	vmovaps	%xmm12, %xmm13
	vfmadd132ps	%xmm0, %xmm2, %xmm13
	vroundps	$9, %xmm13, %xmm13
	vfmsub132ps	%xmm0, %xmm13, %xmm12
	vmovaps	%xmm12, %xmm3
	vfmadd132ps	%xmm1, %xmm8, %xmm3
	vfmadd132ps	%xmm12, %xmm7, %xmm3
	vfmadd132ps	%xmm12, %xmm6, %xmm3
	vfmadd132ps	%xmm12, %xmm5, %xmm3
	vfmadd213ps	.LC188(%rip), %xmm12, %xmm3
	vcvttps2dq	%xmm13, %xmm12
	vpaddd	864(%rsp), %xmm12, %xmm13
	vpslld	$23, %xmm13, %xmm12
	vmulps	.LC218(%rip), %xmm12, %xmm13
	vfmadd132ps	%xmm13, %xmm4, %xmm3
	vrcpps	%xmm3, %xmm12
	vmulps	%xmm3, %xmm12, %xmm13
	vmulps	%xmm13, %xmm12, %xmm13
	vaddps	%xmm12, %xmm12, %xmm12
	vsubps	%xmm13, %xmm12, %xmm13
	vaddps	672(%rsp), %xmm14, %xmm12
	vmulps	%xmm13, %xmm4, %xmm4
	vsubps	(%r12), %xmm4, %xmm13
	vmovaps	768(%rsp), %xmm4
	vmulps	%xmm4, %xmm3, %xmm3
	vmovaps	%xmm4, %xmm14
	vfnmadd132ps	%xmm12, %xmm11, %xmm14
	vfmsub132ps	%xmm4, %xmm11, %xmm12
	vfmadd213ps	(%r12), %xmm3, %xmm13
	vmovaps	%xmm14, 672(%rsp)
	vmovaps	%xmm12, %xmm14
	vmovaps	832(%rsp), %xmm12
	vaddps	.LC199(%rip), %xmm12, %xmm3
	vmulps	.LC200(%rip), %xmm3, %xmm4
	vmovups	%xmm13, (%r12)
	vaddps	%xmm12, %xmm14, %xmm13
	vminps	%xmm10, %xmm4, %xmm11
	vmaxps	%xmm9, %xmm11, %xmm4
	vmovaps	%xmm4, %xmm3
	vfmadd132ps	%xmm0, %xmm2, %xmm3
	vroundps	$9, %xmm3, %xmm3
	vfmsub132ps	%xmm0, %xmm3, %xmm4
	vmovaps	%xmm4, %xmm11
	vfmadd132ps	%xmm1, %xmm8, %xmm11
	vfmadd132ps	%xmm4, %xmm7, %xmm11
	vfmadd132ps	%xmm4, %xmm6, %xmm11
	vfmadd132ps	%xmm4, %xmm5, %xmm11
	vfmadd213ps	.LC188(%rip), %xmm4, %xmm11
	vcvttps2dq	%xmm3, %xmm4
	vpaddd	864(%rsp), %xmm4, %xmm3
	vpslld	$23, %xmm3, %xmm4
	vfmadd213ps	.LC190(%rip), %xmm11, %xmm4
	vrcpps	%xmm4, %xmm11
	vmulps	%xmm4, %xmm11, %xmm3
	vmulps	%xmm3, %xmm11, %xmm4
	vaddps	%xmm11, %xmm11, %xmm11
	vbroadcastss	.LC120(%rip), %xmm3
	vaddps	%xmm12, %xmm3, %xmm12
	vsubps	%xmm4, %xmm11, %xmm11
	vmulps	.LC202(%rip), %xmm12, %xmm4
	vminps	%xmm10, %xmm4, %xmm3
	vmaxps	%xmm9, %xmm3, %xmm4
	vmovaps	%xmm4, %xmm12
	vfmadd132ps	%xmm0, %xmm2, %xmm12
	vroundps	$9, %xmm12, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm4
	vmovaps	%xmm4, %xmm3
	vfmadd132ps	%xmm1, %xmm8, %xmm3
	vfmadd132ps	%xmm4, %xmm7, %xmm3
	vfmadd132ps	%xmm4, %xmm6, %xmm3
	vfmadd132ps	%xmm4, %xmm5, %xmm3
	vfmadd213ps	.LC188(%rip), %xmm4, %xmm3
	vcvttps2dq	%xmm12, %xmm4
	vpaddd	864(%rsp), %xmm4, %xmm12
	vpslld	$23, %xmm12, %xmm4
	vfmadd213ps	.LC190(%rip), %xmm4, %xmm3
	vbroadcastss	.LC122(%rip), %xmm4
	vmulps	%xmm11, %xmm11, %xmm12
	vmulps	%xmm11, %xmm12, %xmm11
	vmulps	%xmm4, %xmm11, %xmm12
	vmulps	(%rbx), %xmm12, %xmm11
	vmovaps	832(%rsp), %xmm12
	vaddps	%xmm12, %xmm15, %xmm15
	vmulps	%xmm15, %xmm11, %xmm15
	vbroadcastss	.LC124(%rip), %xmm11
	vfmadd231ps	%xmm11, %xmm13, %xmm15
	vmovaps	.LC204(%rip), %xmm13
	vaddps	%xmm12, %xmm13, %xmm12
	vmulps	.LC205(%rip), %xmm12, %xmm11
	vminps	%xmm10, %xmm11, %xmm13
	vmaxps	%xmm9, %xmm13, %xmm11
	vmovaps	%xmm11, %xmm12
	vfmadd132ps	%xmm0, %xmm2, %xmm12
	vroundps	$9, %xmm12, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm11
	vcvttps2dq	%xmm12, %xmm12
	vmovaps	%xmm11, %xmm13
	vfmadd132ps	%xmm1, %xmm8, %xmm13
	vfmadd132ps	%xmm11, %xmm7, %xmm13
	vfmadd132ps	%xmm11, %xmm6, %xmm13
	vfmadd132ps	%xmm11, %xmm5, %xmm13
	vfmadd213ps	.LC188(%rip), %xmm13, %xmm11
	vrcpps	%xmm3, %xmm13
	vmulps	%xmm3, %xmm13, %xmm3
	vmulps	%xmm3, %xmm13, %xmm3
	vaddps	%xmm13, %xmm13, %xmm13
	vsubps	%xmm3, %xmm13, %xmm3
	vsubps	(%rbx), %xmm3, %xmm13
	vbroadcastss	348(%rsp), %xmm3
	vmulps	%xmm3, %xmm13, %xmm13
	vpaddd	864(%rsp), %xmm12, %xmm3
	vpslld	$23, %xmm3, %xmm12
	vmulps	%xmm12, %xmm11, %xmm11
	vrcpps	%xmm11, %xmm3
	vmulps	%xmm11, %xmm3, %xmm12
	vmulps	%xmm12, %xmm3, %xmm11
	vaddps	%xmm3, %xmm3, %xmm3
	vsubps	%xmm11, %xmm3, %xmm12
	vmulps	%xmm12, %xmm13, %xmm13
	vaddps	(%rbx), %xmm13, %xmm11
	vmovups	%xmm11, (%rbx)
	vmovups	(%r11), %xmm3
	vmovaps	832(%rsp), %xmm11
	vaddps	.LC174(%rip), %xmm11, %xmm13
	vmulps	%xmm3, %xmm3, %xmm12
	vmulps	%xmm12, %xmm12, %xmm3
	vmulps	%xmm4, %xmm3, %xmm12
	vaddps	.LC214(%rip), %xmm11, %xmm4
	vaddps	.LC215(%rip), %xmm11, %xmm11
	vmulps	%xmm4, %xmm12, %xmm3
	vbroadcastss	.LC126(%rip), %xmm12
	vmulps	.LC207(%rip), %xmm11, %xmm4
	vmulps	.LC216(%rip), %xmm11, %xmm11
	vfmadd132ps	%xmm12, %xmm3, %xmm13
	vminps	%xmm10, %xmm4, %xmm3
	vmaxps	%xmm9, %xmm3, %xmm4
	vaddps	%xmm13, %xmm15, %xmm15
	vmovaps	%xmm4, %xmm12
	vfmadd132ps	%xmm0, %xmm2, %xmm12
	vroundps	$9, %xmm12, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm4
	vmovaps	%xmm4, %xmm3
	vfmadd132ps	%xmm1, %xmm8, %xmm3
	vfmadd132ps	%xmm4, %xmm7, %xmm3
	vfmadd132ps	%xmm4, %xmm6, %xmm3
	vfmadd132ps	%xmm4, %xmm5, %xmm3
	vfmadd213ps	.LC188(%rip), %xmm4, %xmm3
	vcvttps2dq	%xmm12, %xmm4
	vpaddd	864(%rsp), %xmm4, %xmm12
	vpslld	$23, %xmm12, %xmm4
	vfnmadd213ps	.LC190(%rip), %xmm4, %xmm3
	vrcpps	%xmm3, %xmm12
	vmulps	%xmm3, %xmm12, %xmm3
	vaddps	%xmm12, %xmm12, %xmm4
	vmulps	%xmm3, %xmm12, %xmm3
	vsubps	%xmm3, %xmm4, %xmm12
	vmovaps	832(%rsp), %xmm3
	vaddps	.LC198(%rip), %xmm3, %xmm4
	vmulps	%xmm12, %xmm11, %xmm11
	vmulps	.LC217(%rip), %xmm4, %xmm12
	vminps	%xmm10, %xmm12, %xmm3
	vmaxps	%xmm9, %xmm3, %xmm4
	vmovaps	%xmm4, %xmm12
	vfmadd132ps	%xmm0, %xmm2, %xmm12
	vroundps	$9, %xmm12, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm4
	vmovaps	%xmm4, %xmm3
	vfmadd132ps	%xmm1, %xmm8, %xmm3
	vfmadd132ps	%xmm4, %xmm7, %xmm3
	vfmadd132ps	%xmm4, %xmm6, %xmm3
	vfmadd132ps	%xmm4, %xmm5, %xmm3
	vfmadd213ps	.LC188(%rip), %xmm4, %xmm3
	vcvttps2dq	%xmm12, %xmm4
	vpaddd	864(%rsp), %xmm4, %xmm12
	movq	608(%rsp), %rsi
	movq	576(%rsp), %rcx
	vmovaps	832(%rsp), %xmm13
	vpslld	$23, %xmm12, %xmm4
	vmulps	.LC218(%rip), %xmm4, %xmm12
	vfmadd132ps	%xmm12, %xmm11, %xmm3
	vrcpps	%xmm3, %xmm4
	vmulps	%xmm3, %xmm4, %xmm12
	vmulps	%xmm12, %xmm4, %xmm12
	vaddps	%xmm4, %xmm4, %xmm4
	vsubps	%xmm12, %xmm4, %xmm12
	vmovaps	768(%rsp), %xmm4
	vmulps	%xmm4, %xmm3, %xmm3
	vfnmadd231ps	%xmm4, %xmm15, %xmm13
	vbroadcastss	.LC104(%rip), %xmm4
	vmulps	%xmm12, %xmm11, %xmm11
	vsubps	(%r11), %xmm11, %xmm12
	vfmadd213ps	(%r11), %xmm3, %xmm12
	vmovaps	%xmm13, 832(%rsp)
	vmovaps	800(%rsp), %xmm13
	vaddps	.LC175(%rip), %xmm13, %xmm11
	vaddps	%xmm13, %xmm14, %xmm14
	vmovups	%xmm12, (%r11)
	vbroadcastss	.LC128(%rip), %xmm12
	vmulps	%xmm12, %xmm11, %xmm3
	vsubps	%xmm13, %xmm4, %xmm11
	vbroadcastss	.LC130(%rip), %xmm12
	vmovaps	%xmm14, 640(%rsp)
	vmovups	(%rsi), %xmm14
	vmulps	%xmm14, %xmm14, %xmm15
	vmulps	%xmm15, %xmm3, %xmm15
	vmulps	%xmm12, %xmm11, %xmm3
	vminps	%xmm10, %xmm3, %xmm4
	vmaxps	%xmm9, %xmm4, %xmm3
	vmovaps	%xmm3, %xmm4
	vfmadd132ps	%xmm0, %xmm2, %xmm4
	vroundps	$9, %xmm4, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm3
	vmovaps	%xmm3, %xmm11
	vfmadd132ps	%xmm1, %xmm8, %xmm11
	vfmadd132ps	%xmm3, %xmm7, %xmm11
	vfmadd132ps	%xmm3, %xmm6, %xmm11
	vfmadd132ps	%xmm3, %xmm5, %xmm11
	vfmadd213ps	.LC188(%rip), %xmm3, %xmm11
	vcvttps2dq	%xmm12, %xmm3
	vpaddd	864(%rsp), %xmm3, %xmm4
	vpslld	$23, %xmm4, %xmm12
	vfmadd213ps	.LC190(%rip), %xmm11, %xmm12
	vrcpps	%xmm12, %xmm11
	vmulps	%xmm12, %xmm11, %xmm3
	vaddps	%xmm11, %xmm11, %xmm4
	vmulps	%xmm3, %xmm11, %xmm12
	vbroadcastss	.LC132(%rip), %xmm11
	vsubps	%xmm12, %xmm4, %xmm3
	vbroadcastss	.LC134(%rip), %xmm12
	vaddps	%xmm13, %xmm12, %xmm12
	vbroadcastss	.LC25(%rip), %xmm13
	vmulps	%xmm3, %xmm11, %xmm11
	vmulps	%xmm13, %xmm12, %xmm4
	vminps	%xmm10, %xmm4, %xmm3
	vmaxps	%xmm9, %xmm3, %xmm3
	vmovaps	%xmm3, %xmm13
	vfmadd132ps	%xmm0, %xmm2, %xmm13
	vroundps	$9, %xmm13, %xmm4
	vfmsub132ps	%xmm0, %xmm4, %xmm3
	vcvttps2dq	%xmm4, %xmm4
	vmovaps	%xmm3, %xmm13
	vfmadd132ps	%xmm1, %xmm8, %xmm13
	vfmadd132ps	%xmm3, %xmm7, %xmm13
	vfmadd132ps	%xmm3, %xmm6, %xmm13
	vfmadd132ps	%xmm3, %xmm5, %xmm13
	vfmadd213ps	.LC188(%rip), %xmm13, %xmm3
	vpaddd	864(%rsp), %xmm4, %xmm13
	vpslld	$23, %xmm13, %xmm4
	vbroadcastss	.LC137(%rip), %xmm13
	vfmadd231ps	%xmm4, %xmm3, %xmm13
	vbroadcastss	.LC139(%rip), %xmm3
	vmulps	%xmm3, %xmm12, %xmm12
	vrcpps	%xmm13, %xmm4
	vmulps	%xmm13, %xmm4, %xmm13
	vmulps	%xmm13, %xmm4, %xmm3
	vaddps	%xmm4, %xmm4, %xmm4
	vsubps	%xmm3, %xmm4, %xmm13
	vmulps	%xmm13, %xmm12, %xmm12
	vaddps	%xmm11, %xmm12, %xmm3
	vrcpps	%xmm3, %xmm4
	vmulps	%xmm3, %xmm4, %xmm13
	vmulps	%xmm13, %xmm4, %xmm12
	vaddps	%xmm4, %xmm4, %xmm4
	vsubps	%xmm12, %xmm4, %xmm13
	vbroadcastss	368(%rsp), %xmm4
	vmulps	%xmm4, %xmm3, %xmm3
	vmulps	%xmm13, %xmm11, %xmm11
	vmovaps	800(%rsp), %xmm13
	vsubps	%xmm14, %xmm11, %xmm12
	vfmadd132ps	%xmm3, %xmm14, %xmm12
	vmovups	%xmm12, (%rsi)
	vaddps	.LC174(%rip), %xmm13, %xmm12
	vmovups	(%rcx), %xmm14
	vaddps	.LC214(%rip), %xmm13, %xmm11
	vmulps	.LC198(%rip), %xmm14, %xmm4
	vbroadcastss	.LC141(%rip), %xmm13
	vmulps	%xmm4, %xmm11, %xmm3
	vbroadcastss	.LC143(%rip), %xmm11
	vbroadcastss	.LC145(%rip), %xmm4
	vfmadd132ps	%xmm13, %xmm3, %xmm12
	vbroadcastss	.LC147(%rip), %xmm13
	vmulps	(%rdx), %xmm11, %xmm3
	vminps	%xmm4, %xmm3, %xmm3
	vaddps	%xmm13, %xmm3, %xmm11
	vrcpps	%xmm11, %xmm4
	vmulps	%xmm11, %xmm4, %xmm13
	vmulps	768(%rsp), %xmm11, %xmm11
	vmulps	%xmm13, %xmm4, %xmm13
	vaddps	%xmm4, %xmm4, %xmm4
	vsubps	%xmm13, %xmm4, %xmm13
	vmulps	%xmm13, %xmm3, %xmm3
	vmovaps	800(%rsp), %xmm13
	vsubps	%xmm14, %xmm3, %xmm4
	vbroadcastss	516(%rsp), %xmm3
	vfmadd132ps	%xmm11, %xmm14, %xmm4
	vbroadcastss	.LC149(%rip), %xmm14
	vaddps	%xmm13, %xmm14, %xmm14
	vmovups	%xmm4, (%rcx)
	vbroadcastss	.LC151(%rip), %xmm4
	vmulps	(%r8), %xmm4, %xmm11
	vbroadcastss	.LC153(%rip), %xmm4
	vfmadd132ps	%xmm11, %xmm3, %xmm14
	vbroadcastss	.LC155(%rip), %xmm11
	vaddps	%xmm14, %xmm12, %xmm14
	vaddps	%xmm13, %xmm4, %xmm12
	vmulps	%xmm11, %xmm12, %xmm3
	vminps	%xmm10, %xmm3, %xmm4
	vmaxps	%xmm9, %xmm4, %xmm12
	vmovaps	%xmm12, %xmm11
	vfmadd132ps	%xmm0, %xmm2, %xmm11
	vroundps	$9, %xmm11, %xmm4
	vfmsub132ps	%xmm0, %xmm4, %xmm12
	vmovaps	%xmm12, %xmm3
	vfmadd132ps	%xmm1, %xmm8, %xmm3
	vfmadd132ps	%xmm12, %xmm7, %xmm3
	vfmadd132ps	%xmm12, %xmm6, %xmm3
	vfmadd132ps	%xmm12, %xmm5, %xmm3
	vfmadd213ps	.LC188(%rip), %xmm12, %xmm3
	vcvttps2dq	%xmm4, %xmm12
	vpaddd	864(%rsp), %xmm12, %xmm11
	vbroadcastss	.LC157(%rip), %xmm12
	vpslld	$23, %xmm11, %xmm4
	vbroadcastss	.LC159(%rip), %xmm11
	vfmadd213ps	.LC190(%rip), %xmm4, %xmm3
	vfmadd132ps	%xmm13, %xmm11, %xmm12
	vminps	%xmm10, %xmm12, %xmm13
	vmaxps	%xmm9, %xmm13, %xmm4
	vbroadcastss	.LC163(%rip), %xmm13
	vmovaps	%xmm4, %xmm12
	vfmadd132ps	%xmm0, %xmm2, %xmm12
	vroundps	$9, %xmm12, %xmm12
	vfmsub132ps	%xmm0, %xmm12, %xmm4
	vmovaps	%xmm4, %xmm11
	vfmadd132ps	%xmm1, %xmm8, %xmm11
	vfmadd132ps	%xmm4, %xmm7, %xmm11
	vfmadd132ps	%xmm4, %xmm6, %xmm11
	vfmadd132ps	%xmm4, %xmm5, %xmm11
	vfmadd213ps	.LC188(%rip), %xmm11, %xmm4
	vbroadcastss	.LC161(%rip), %xmm11
	vfmadd132ps	800(%rsp), %xmm13, %xmm11
	vminps	%xmm10, %xmm11, %xmm10
	vmaxps	%xmm9, %xmm10, %xmm9
	vfmadd231ps	%xmm0, %xmm9, %xmm2
	vroundps	$9, %xmm2, %xmm2
	vfmsub132ps	%xmm0, %xmm2, %xmm9
	vmovdqa	864(%rsp), %xmm0
	vfmadd132ps	%xmm9, %xmm8, %xmm1
	vcvttps2dq	%xmm12, %xmm8
	vfmadd132ps	%xmm9, %xmm7, %xmm1
	vpaddd	%xmm0, %xmm8, %xmm7
	vmovaps	768(%rsp), %xmm8
	vfmadd132ps	%xmm9, %xmm6, %xmm1
	vpslld	$23, %xmm7, %xmm6
	vbroadcastss	372(%rsp), %xmm7
	vfmadd132ps	%xmm9, %xmm5, %xmm1
	vcvttps2dq	%xmm2, %xmm5
	vpaddd	%xmm0, %xmm5, %xmm12
	vfmadd213ps	.LC188(%rip), %xmm9, %xmm1
	vpslld	$23, %xmm12, %xmm11
	vmulps	%xmm11, %xmm1, %xmm1
	vfmadd231ps	%xmm6, %xmm4, %xmm1
	vrcpps	%xmm3, %xmm4
	vmulps	%xmm3, %xmm4, %xmm3
	vaddps	%xmm4, %xmm4, %xmm10
	vmulps	%xmm8, %xmm1, %xmm0
	vmulps	%xmm3, %xmm4, %xmm13
	vsubps	%xmm13, %xmm10, %xmm9
	vsubps	(%r8), %xmm9, %xmm2
	vfmadd213ps	(%r8), %xmm0, %xmm2
	vmovups	%xmm2, (%r8)
	vbroadcastss	520(%rsp), %xmm6
	movl	544(%rsp), %r14d
	vmovaps	800(%rsp), %xmm5
	vbroadcastss	.LC169(%rip), %xmm1
	vbroadcastss	.LC165(%rip), %xmm12
	vmulps	(%rdx), %xmm1, %xmm4
	movl	%r14d, %r13d
	vfmsub132ps	%xmm5, %xmm6, %xmm7
	andl	$-4, %r13d
	vbroadcastss	.LC171(%rip), %xmm3
	vbroadcastss	.LC167(%rip), %xmm11
	vmovaps	832(%rsp), %xmm10
	addl	%r13d, 524(%rsp)
	andl	$3, %r14d
	vfmadd132ps	%xmm12, %xmm15, %xmm7
	vfmsub132ps	%xmm3, %xmm4, %xmm15
	vfmadd213ps	(%rdx), %xmm8, %xmm15
	vfmadd231ps	640(%rsp), %xmm11, %xmm7
	vmovups	%xmm15, (%rdx)
	vaddps	%xmm7, %xmm14, %xmm15
	vmovaps	672(%rsp), %xmm14
	vmovups	%xmm14, (%rdi)
	movq	704(%rsp), %rdi
	vfnmadd132ps	%xmm15, %xmm5, %xmm8
	vmovups	%xmm10, (%rdi)
	vmovups	%xmm8, (%r9)
	je	.L30
.L32:
	movslq	524(%rsp), %rax
	vmovss	.LC41(%rip), %xmm4
	vmovss	.LC43(%rip), %xmm3
	vmovss	.LC45(%rip), %xmm0
	vmovss	.LC47(%rip), %xmm2
	vmovss	.LC55(%rip), %xmm9
	vmovss	.LC57(%rip), %xmm8
	vmovss	.LC59(%rip), %xmm15
	vmovss	.LC62(%rip), %xmm5
	movq	96(%rsp), %r14
	movq	88(%rsp), %r8
	movq	80(%rsp), %r9
	movq	72(%rsp), %r10
	movq	64(%rsp), %r11
	movq	56(%rsp), %rbx
	movq	48(%rsp), %r12
	movq	40(%rsp), %rdi
	movq	32(%rsp), %r13
	.p2align 4,,10
	.p2align 3
.L34:
	movq	744(%rsp), %rdx
	movq	752(%rsp), %rcx
	vmovss	0(%r13,%rax,4), %xmm13
	movq	536(%rsp), %rsi
	vmovss	(%rdx,%rax,4), %xmm6
	vmovss	(%rcx,%rax,4), %xmm7
	vmovss	(%rsi,%rax,4), %xmm11
	movq	360(%rsp), %rdx
	vsubss	%xmm7, %xmm6, %xmm14
	vsubss	.LC246(%rip), %xmm6, %xmm10
	vmovss	%xmm7, 864(%rsp)
	vmulss	%xmm13, %xmm13, %xmm7
	vsubss	%xmm11, %xmm6, %xmm12
	vmulss	.LC27(%rip), %xmm12, %xmm1
	vfmadd132ss	.LC29(%rip), %xmm1, %xmm14
	vmulss	%xmm13, %xmm7, %xmm12
	vmulss	(%rdi,%rax,4), %xmm12, %xmm1
	vsubss	.LC247(%rip), %xmm6, %xmm12
	vmulss	(%rdx,%rax,4), %xmm1, %xmm7
	vmulss	%xmm12, %xmm7, %xmm1
	vfmadd132ss	.LC35(%rip), %xmm1, %xmm10
	vaddss	%xmm10, %xmm14, %xmm14
	vaddss	.LC37(%rip), %xmm6, %xmm10
	vmulss	.LC39(%rip), %xmm10, %xmm7
	vmovss	%xmm14, 800(%rsp)
	vminss	%xmm4, %xmm7, %xmm12
	vmovss	.LC49(%rip), %xmm7
	vmaxss	%xmm3, %xmm12, %xmm1
	vaddss	.LC64(%rip), %xmm6, %xmm12
	vmovaps	%xmm1, %xmm10
	vfmadd132ss	%xmm0, %xmm2, %xmm10
	vroundss	$9, %xmm10, %xmm10, %xmm10
	vfmsub132ss	%xmm0, %xmm10, %xmm1
	vcvttss2sil	%xmm10, %esi
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm7
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm7
	addl	$127, %esi
	sall	$23, %esi
	vmovd	%esi, %xmm14
	vfmadd132ss	%xmm1, %xmm9, %xmm7
	vfmadd132ss	%xmm1, %xmm8, %xmm7
	vfmadd132ss	%xmm1, %xmm15, %xmm7
	vmulss	.LC66(%rip), %xmm12, %xmm1
	vmovss	.LC49(%rip), %xmm12
	vfmadd132ss	%xmm14, %xmm5, %xmm7
	vminss	%xmm4, %xmm1, %xmm10
	vmaxss	%xmm3, %xmm10, %xmm1
	vdivss	%xmm7, %xmm5, %xmm7
	vmovaps	%xmm1, %xmm14
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm1
	vcvttss2sil	%xmm14, %ecx
	vaddss	.LC68(%rip), %xmm6, %xmm14
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm12
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm12
	addl	$127, %ecx
	sall	$23, %ecx
	vmovd	%ecx, %xmm10
	vfmadd132ss	%xmm1, %xmm9, %xmm12
	vfmadd132ss	%xmm1, %xmm8, %xmm12
	vfmadd132ss	%xmm12, %xmm15, %xmm1
	vmulss	.LC70(%rip), %xmm14, %xmm12
	vfmadd132ss	%xmm10, %xmm5, %xmm1
	vminss	%xmm4, %xmm12, %xmm10
	vmovss	.LC49(%rip), %xmm12
	vmaxss	%xmm3, %xmm10, %xmm10
	vmovaps	%xmm10, %xmm14
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm10
	vcvttss2sil	%xmm14, %edx
	vfmadd213ss	.LC51(%rip), %xmm10, %xmm12
	vfmadd213ss	.LC53(%rip), %xmm10, %xmm12
	addl	$127, %edx
	sall	$23, %edx
	vfmadd132ss	%xmm10, %xmm9, %xmm12
	vfmadd132ss	%xmm10, %xmm8, %xmm12
	vfmadd132ss	%xmm10, %xmm15, %xmm12
	vmovd	%edx, %xmm10
	vmulss	.LC72(%rip), %xmm10, %xmm14
	vaddss	.LC74(%rip), %xmm6, %xmm10
	vmulss	%xmm12, %xmm14, %xmm12
	vmulss	.LC76(%rip), %xmm10, %xmm14
	vmovd	%xmm12, %esi
	vminss	%xmm4, %xmm14, %xmm12
	vmovss	.LC49(%rip), %xmm14
	vmaxss	%xmm3, %xmm12, %xmm10
	vmovaps	%xmm10, %xmm12
	vfmadd132ss	%xmm0, %xmm2, %xmm12
	vroundss	$9, %xmm12, %xmm12, %xmm12
	vfmsub132ss	%xmm0, %xmm12, %xmm10
	vcvttss2sil	%xmm12, %ecx
	vfmadd213ss	.LC51(%rip), %xmm10, %xmm14
	vfmadd213ss	.LC53(%rip), %xmm10, %xmm14
	addl	$127, %ecx
	sall	$23, %ecx
	vmovd	%ecx, %xmm12
	vfmadd132ss	%xmm10, %xmm9, %xmm14
	vfmadd132ss	%xmm10, %xmm8, %xmm14
	vfmadd132ss	%xmm10, %xmm15, %xmm14
	vsubss	%xmm13, %xmm7, %xmm10
	vfmadd132ss	%xmm14, %xmm5, %xmm12
	vmovss	764(%rsp), %xmm14
	vfmadd132ss	%xmm14, %xmm13, %xmm10
	vdivss	%xmm1, %xmm5, %xmm13
	vmovss	%xmm10, 0(%r13,%rax,4)
	vmovd	%esi, %xmm10
	vmovss	(%rdi,%rax,4), %xmm7
	vdivss	%xmm12, %xmm10, %xmm12
	vsubss	%xmm7, %xmm13, %xmm1
	vmulss	%xmm14, %xmm1, %xmm14
	vaddss	.LC78(%rip), %xmm12, %xmm13
	vdivss	%xmm13, %xmm14, %xmm1
	vaddss	.LC80(%rip), %xmm6, %xmm14
	vmulss	.LC82(%rip), %xmm14, %xmm10
	vminss	%xmm4, %xmm10, %xmm12
	vaddss	.LC84(%rip), %xmm6, %xmm10
	vaddss	%xmm7, %xmm1, %xmm7
	vmaxss	%xmm3, %xmm12, %xmm1
	vmulss	.LC86(%rip), %xmm10, %xmm12
	vmovaps	%xmm1, %xmm14
	vmovss	%xmm7, (%rdi,%rax,4)
	vmovss	.LC49(%rip), %xmm7
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm1
	vcvttss2sil	%xmm14, %edx
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm7
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm7
	addl	$127, %edx
	sall	$23, %edx
	vmovd	%edx, %xmm13
	vfmadd132ss	%xmm1, %xmm9, %xmm7
	vfmadd132ss	%xmm1, %xmm8, %xmm7
	vfmadd132ss	%xmm1, %xmm15, %xmm7
	vminss	%xmm4, %xmm12, %xmm1
	vfmadd132ss	%xmm13, %xmm5, %xmm7
	vdivss	%xmm7, %xmm5, %xmm14
	vmaxss	%xmm3, %xmm1, %xmm7
	vmovss	.LC49(%rip), %xmm1
	vmovaps	%xmm7, %xmm13
	vfmadd132ss	%xmm0, %xmm2, %xmm13
	vroundss	$9, %xmm13, %xmm13, %xmm13
	vfmsub132ss	%xmm0, %xmm13, %xmm7
	vcvttss2sil	%xmm13, %esi
	vmovss	(%r12,%rax,4), %xmm13
	vfmadd213ss	.LC51(%rip), %xmm7, %xmm1
	vfmadd213ss	.LC53(%rip), %xmm7, %xmm1
	addl	$127, %esi
	sall	$23, %esi
	vmovd	%esi, %xmm10
	vfmadd132ss	%xmm7, %xmm9, %xmm1
	vmulss	%xmm14, %xmm14, %xmm12
	vfmadd132ss	%xmm7, %xmm8, %xmm1
	vmulss	%xmm14, %xmm12, %xmm14
	vaddss	.LC90(%rip), %xmm6, %xmm12
	vfmadd132ss	%xmm7, %xmm15, %xmm1
	vmulss	.LC88(%rip), %xmm14, %xmm7
	vmulss	.LC92(%rip), %xmm12, %xmm14
	vfmadd132ss	%xmm10, %xmm5, %xmm1
	vmulss	%xmm13, %xmm7, %xmm10
	vminss	%xmm4, %xmm14, %xmm7
	vmaxss	%xmm3, %xmm7, %xmm14
	vdivss	%xmm1, %xmm5, %xmm1
	vmovss	%xmm10, 832(%rsp)
	vmovss	.LC49(%rip), %xmm10
	vmovaps	%xmm14, %xmm12
	vfmadd132ss	%xmm0, %xmm2, %xmm12
	vroundss	$9, %xmm12, %xmm12, %xmm12
	vfmsub132ss	%xmm0, %xmm12, %xmm14
	vcvttss2sil	%xmm12, %ecx
	vfmadd213ss	.LC51(%rip), %xmm14, %xmm10
	vfmadd213ss	.LC53(%rip), %xmm14, %xmm10
	addl	$127, %ecx
	sall	$23, %ecx
	vmovd	%ecx, %xmm12
	vfmadd132ss	%xmm14, %xmm9, %xmm10
	vsubss	%xmm13, %xmm1, %xmm7
	vfmadd132ss	%xmm14, %xmm8, %xmm10
	vfmadd132ss	%xmm14, %xmm15, %xmm10
	vmulss	344(%rsp), %xmm7, %xmm14
	vmulss	%xmm12, %xmm10, %xmm10
	vdivss	%xmm10, %xmm14, %xmm1
	vaddss	%xmm13, %xmm1, %xmm13
	vmovss	%xmm13, (%r12,%rax,4)
	vmovss	(%rbx,%rax,4), %xmm13
	vaddss	.LC94(%rip), %xmm6, %xmm14
	vmulss	.LC96(%rip), %xmm14, %xmm10
	vmulss	%xmm13, %xmm13, %xmm7
	vminss	%xmm4, %xmm10, %xmm1
	vmulss	%xmm7, %xmm7, %xmm12
	vmovss	.LC49(%rip), %xmm7
	vmaxss	%xmm3, %xmm1, %xmm1
	vmovaps	%xmm1, %xmm10
	vfmadd132ss	%xmm0, %xmm2, %xmm10
	vroundss	$9, %xmm10, %xmm10, %xmm10
	vfmsub132ss	%xmm0, %xmm10, %xmm1
	vcvttss2sil	%xmm10, %edx
	vaddss	.LC98(%rip), %xmm6, %xmm10
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm7
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm7
	addl	$127, %edx
	sall	$23, %edx
	vmovd	%edx, %xmm14
	vfmadd132ss	%xmm1, %xmm9, %xmm7
	vfmadd132ss	%xmm1, %xmm8, %xmm7
	vfmadd132ss	%xmm7, %xmm15, %xmm1
	vmulss	.LC100(%rip), %xmm10, %xmm7
	vmovss	.LC49(%rip), %xmm10
	vfmadd132ss	%xmm14, %xmm5, %xmm1
	vminss	%xmm4, %xmm7, %xmm14
	vmaxss	%xmm3, %xmm14, %xmm7
	vdivss	%xmm1, %xmm5, %xmm1
	vmovaps	%xmm7, %xmm14
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm7
	vcvttss2sil	%xmm14, %esi
	vfmadd213ss	.LC51(%rip), %xmm7, %xmm10
	vfmadd213ss	.LC53(%rip), %xmm7, %xmm10
	addl	$127, %esi
	sall	$23, %esi
	vfmadd132ss	%xmm7, %xmm9, %xmm10
	vfmadd132ss	%xmm7, %xmm8, %xmm10
	vfmadd132ss	%xmm7, %xmm15, %xmm10
	vmovd	%esi, %xmm7
	vmulss	.LC102(%rip), %xmm7, %xmm14
	vfmadd213ss	.LC104(%rip), %xmm10, %xmm14
	vsubss	%xmm13, %xmm1, %xmm10
	vmulss	764(%rsp), %xmm10, %xmm7
	vdivss	%xmm14, %xmm7, %xmm14
	vaddss	%xmm13, %xmm14, %xmm13
	vmovss	%xmm13, (%rbx,%rax,4)
	vmovss	(%r11,%rax,4), %xmm10
	vaddss	.LC110(%rip), %xmm6, %xmm13
	vmulss	%xmm10, %xmm10, %xmm1
	vmulss	%xmm1, %xmm1, %xmm7
	vmulss	.LC104(%rip), %xmm7, %xmm14
	vaddss	.LC112(%rip), %xmm6, %xmm7
	vfmadd231ss	.LC106(%rip), %xmm12, %xmm14
	vsubss	.LC248(%rip), %xmm6, %xmm12
	vmulss	%xmm14, %xmm13, %xmm1
	vmulss	.LC96(%rip), %xmm7, %xmm14
	vfmadd132ss	832(%rsp), %xmm1, %xmm12
	vmulss	.LC114(%rip), %xmm7, %xmm7
	vminss	%xmm4, %xmm14, %xmm13
	vmaxss	%xmm3, %xmm13, %xmm1
	vmovss	.LC49(%rip), %xmm13
	vmovaps	%xmm1, %xmm14
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm1
	vcvttss2sil	%xmm14, %ecx
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm13
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm13
	addl	$127, %ecx
	sall	$23, %ecx
	vmovd	%ecx, %xmm14
	vfmadd132ss	%xmm1, %xmm9, %xmm13
	vfmadd132ss	%xmm1, %xmm8, %xmm13
	vfmadd132ss	%xmm13, %xmm15, %xmm1
	vfnmadd132ss	%xmm14, %xmm5, %xmm1
	vdivss	%xmm1, %xmm7, %xmm7
	vaddss	.LC78(%rip), %xmm6, %xmm1
	vmulss	.LC116(%rip), %xmm1, %xmm13
	vminss	%xmm4, %xmm13, %xmm14
	vmovss	.LC49(%rip), %xmm13
	vmaxss	%xmm3, %xmm14, %xmm1
	vmovaps	%xmm1, %xmm14
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm1
	vcvttss2sil	%xmm14, %edx
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm13
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm13
	addl	$127, %edx
	sall	$23, %edx
	vfmadd132ss	%xmm1, %xmm9, %xmm13
	vfmadd132ss	%xmm1, %xmm8, %xmm13
	vfmadd132ss	%xmm1, %xmm15, %xmm13
	vmovd	%edx, %xmm1
	vmulss	.LC118(%rip), %xmm1, %xmm1
	vmovss	764(%rsp), %xmm14
	vfmadd132ss	%xmm13, %xmm7, %xmm1
	vdivss	%xmm1, %xmm7, %xmm7
	vmulss	%xmm14, %xmm1, %xmm1
	vsubss	%xmm10, %xmm7, %xmm13
	vfmadd132ss	%xmm1, %xmm10, %xmm13
	vmovss	.LC49(%rip), %xmm1
	vaddss	800(%rsp), %xmm12, %xmm10
	vmovaps	%xmm14, %xmm12
	vfnmadd132ss	%xmm10, %xmm6, %xmm12
	vfmsub132ss	%xmm14, %xmm6, %xmm10
	vaddss	.LC80(%rip), %xmm11, %xmm6
	vmulss	.LC82(%rip), %xmm6, %xmm7
	vmovss	%xmm13, (%r11,%rax,4)
	vmovss	%xmm12, 832(%rsp)
	vaddss	%xmm10, %xmm11, %xmm12
	vmovss	%xmm10, 800(%rsp)
	vminss	%xmm4, %xmm7, %xmm13
	vmaxss	%xmm3, %xmm13, %xmm14
	vaddss	.LC120(%rip), %xmm11, %xmm13
	vmovaps	%xmm14, %xmm7
	vfmadd132ss	%xmm0, %xmm2, %xmm7
	vroundss	$9, %xmm7, %xmm7, %xmm7
	vfmsub132ss	%xmm0, %xmm7, %xmm14
	vcvttss2sil	%xmm7, %esi
	vfmadd213ss	.LC51(%rip), %xmm14, %xmm1
	vfmadd213ss	.LC53(%rip), %xmm14, %xmm1
	addl	$127, %esi
	sall	$23, %esi
	vmovd	%esi, %xmm10
	vfmadd132ss	%xmm14, %xmm9, %xmm1
	vfmadd132ss	%xmm14, %xmm8, %xmm1
	vfmadd132ss	%xmm14, %xmm15, %xmm1
	vmulss	.LC86(%rip), %xmm13, %xmm14
	vfmadd132ss	%xmm10, %xmm5, %xmm1
	vminss	%xmm4, %xmm14, %xmm7
	vmaxss	%xmm3, %xmm7, %xmm14
	vdivss	%xmm1, %xmm5, %xmm6
	vmovss	.LC49(%rip), %xmm1
	vmovaps	%xmm14, %xmm10
	vfmadd132ss	%xmm0, %xmm2, %xmm10
	vroundss	$9, %xmm10, %xmm10, %xmm10
	vfmsub132ss	%xmm0, %xmm10, %xmm14
	vcvttss2sil	%xmm10, %ecx
	vfmadd213ss	.LC51(%rip), %xmm14, %xmm1
	vfmadd213ss	.LC53(%rip), %xmm14, %xmm1
	addl	$127, %ecx
	sall	$23, %ecx
	vmovd	%ecx, %xmm13
	vfmadd132ss	%xmm14, %xmm9, %xmm1
	vmulss	%xmm6, %xmm6, %xmm7
	vfmadd132ss	%xmm14, %xmm8, %xmm1
	vmulss	%xmm6, %xmm7, %xmm6
	vsubss	.LC248(%rip), %xmm11, %xmm7
	vmulss	.LC122(%rip), %xmm6, %xmm10
	vfmadd132ss	%xmm14, %xmm15, %xmm1
	vmovss	(%r10,%rax,4), %xmm14
	vfmadd132ss	%xmm13, %xmm5, %xmm1
	vmulss	%xmm14, %xmm10, %xmm13
	vaddss	.LC90(%rip), %xmm11, %xmm10
	vdivss	%xmm1, %xmm5, %xmm1
	vmulss	%xmm7, %xmm13, %xmm6
	vmulss	.LC92(%rip), %xmm10, %xmm13
	vfmadd132ss	.LC124(%rip), %xmm6, %xmm12
	vminss	%xmm4, %xmm13, %xmm7
	vmovss	.LC49(%rip), %xmm13
	vmaxss	%xmm3, %xmm7, %xmm6
	vmovaps	%xmm6, %xmm10
	vfmadd132ss	%xmm0, %xmm2, %xmm10
	vsubss	%xmm14, %xmm1, %xmm7
	vmulss	348(%rsp), %xmm7, %xmm1
	vsubss	.LC246(%rip), %xmm11, %xmm7
	vroundss	$9, %xmm10, %xmm10, %xmm10
	vfmsub132ss	%xmm0, %xmm10, %xmm6
	vcvttss2sil	%xmm10, %edx
	vfmadd213ss	.LC51(%rip), %xmm6, %xmm13
	vfmadd213ss	.LC53(%rip), %xmm6, %xmm13
	addl	$127, %edx
	sall	$23, %edx
	vfmadd132ss	%xmm6, %xmm9, %xmm13
	vfmadd132ss	%xmm6, %xmm8, %xmm13
	vfmadd132ss	%xmm6, %xmm15, %xmm13
	vmovd	%edx, %xmm6
	vmulss	%xmm6, %xmm13, %xmm10
	vdivss	%xmm10, %xmm1, %xmm13
	vaddss	%xmm14, %xmm13, %xmm14
	vmovss	%xmm14, (%r10,%rax,4)
	vmovss	(%r9,%rax,4), %xmm10
	vaddss	.LC110(%rip), %xmm11, %xmm14
	vmulss	%xmm10, %xmm10, %xmm1
	vmulss	%xmm1, %xmm1, %xmm6
	vmulss	.LC122(%rip), %xmm6, %xmm13
	vaddss	.LC112(%rip), %xmm11, %xmm6
	vmulss	%xmm14, %xmm13, %xmm1
	vfmadd132ss	.LC126(%rip), %xmm1, %xmm7
	vmulss	.LC96(%rip), %xmm6, %xmm13
	vmulss	.LC114(%rip), %xmm6, %xmm6
	vaddss	%xmm12, %xmm7, %xmm12
	vmovss	864(%rsp), %xmm7
	vminss	%xmm4, %xmm13, %xmm14
	vmovss	.LC49(%rip), %xmm13
	vmaxss	%xmm3, %xmm14, %xmm1
	vmovaps	%xmm1, %xmm14
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm1
	vcvttss2sil	%xmm14, %esi
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm13
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm13
	addl	$127, %esi
	sall	$23, %esi
	vmovd	%esi, %xmm14
	vfmadd132ss	%xmm1, %xmm9, %xmm13
	vfmadd132ss	%xmm1, %xmm8, %xmm13
	vfmadd132ss	%xmm13, %xmm15, %xmm1
	vfnmadd132ss	%xmm14, %xmm5, %xmm1
	vdivss	%xmm1, %xmm6, %xmm6
	vaddss	.LC78(%rip), %xmm11, %xmm1
	vmulss	.LC116(%rip), %xmm1, %xmm13
	vminss	%xmm4, %xmm13, %xmm14
	vmovss	.LC49(%rip), %xmm13
	vmaxss	%xmm3, %xmm14, %xmm1
	vmovaps	%xmm1, %xmm14
	vfmadd132ss	%xmm0, %xmm2, %xmm14
	vroundss	$9, %xmm14, %xmm14, %xmm14
	vfmsub132ss	%xmm0, %xmm14, %xmm1
	vcvttss2sil	%xmm14, %ecx
	vfmadd213ss	.LC51(%rip), %xmm1, %xmm13
	vfmadd213ss	.LC53(%rip), %xmm1, %xmm13
	addl	$127, %ecx
	sall	$23, %ecx
	vfmadd132ss	%xmm1, %xmm9, %xmm13
	vfmadd132ss	%xmm1, %xmm8, %xmm13
	vfmadd132ss	%xmm1, %xmm15, %xmm13
	vmovd	%ecx, %xmm1
	vmulss	.LC118(%rip), %xmm1, %xmm1
	vfmadd132ss	%xmm13, %xmm6, %xmm1
	vdivss	%xmm1, %xmm6, %xmm6
	vsubss	%xmm10, %xmm6, %xmm13
	vmovss	764(%rsp), %xmm6
	vmulss	%xmm6, %xmm1, %xmm14
	vfnmadd132ss	%xmm6, %xmm11, %xmm12
	vmovss	800(%rsp), %xmm11
	vmovss	.LC104(%rip), %xmm6
	vsubss	.LC247(%rip), %xmm7, %xmm1
	vfmadd132ss	%xmm14, %xmm10, %xmm13
	vaddss	%xmm7, %xmm11, %xmm10
	vsubss	%xmm7, %xmm6, %xmm11
	vmovd	%xmm12, %edx
	vmovss	%xmm10, 800(%rsp)
	vmulss	.LC130(%rip), %xmm11, %xmm10
	vmovss	%xmm13, (%r9,%rax,4)
	vmovss	(%r8,%rax,4), %xmm12
	vmulss	.LC128(%rip), %xmm1, %xmm13
	vmulss	%xmm12, %xmm12, %xmm14
	vminss	%xmm4, %xmm10, %xmm1
	vmovss	.LC49(%rip), %xmm10
	vmulss	%xmm14, %xmm13, %xmm14
	vmaxss	%xmm3, %xmm1, %xmm13
	vmovss	.LC132(%rip), %xmm1
	vmovaps	%xmm13, %xmm6
	vfmadd132ss	%xmm0, %xmm2, %xmm6
	vroundss	$9, %xmm6, %xmm6, %xmm6
	vfmsub132ss	%xmm0, %xmm6, %xmm13
	vcvttss2sil	%xmm6, %esi
	vfmadd213ss	.LC51(%rip), %xmm13, %xmm10
	vfmadd213ss	.LC53(%rip), %xmm13, %xmm10
	addl	$127, %esi
	sall	$23, %esi
	vmovd	%esi, %xmm11
	vfmadd132ss	%xmm13, %xmm9, %xmm10
	vfmadd132ss	%xmm13, %xmm8, %xmm10
	vfmadd132ss	%xmm13, %xmm15, %xmm10
	vmovss	.LC134(%rip), %xmm13
	vfmadd132ss	%xmm11, %xmm5, %xmm10
	vdivss	%xmm10, %xmm1, %xmm1
	vaddss	%xmm7, %xmm13, %xmm10
	vmulss	.LC25(%rip), %xmm10, %xmm6
	vmulss	.LC139(%rip), %xmm10, %xmm10
	vminss	%xmm4, %xmm6, %xmm11
	vmaxss	%xmm3, %xmm11, %xmm6
	vmovss	.LC49(%rip), %xmm11
	vmovaps	%xmm6, %xmm13
	vfmadd132ss	%xmm0, %xmm2, %xmm13
	vroundss	$9, %xmm13, %xmm13, %xmm13
	vfmsub132ss	%xmm0, %xmm13, %xmm6
	vcvttss2sil	%xmm13, %ecx
	vfmadd213ss	.LC51(%rip), %xmm6, %xmm11
	vfmadd213ss	.LC53(%rip), %xmm6, %xmm11
	addl	$127, %ecx
	sall	$23, %ecx
	vmovd	%ecx, %xmm13
	vfmadd132ss	%xmm6, %xmm9, %xmm11
	vfmadd132ss	%xmm6, %xmm8, %xmm11
	vfmadd132ss	%xmm11, %xmm15, %xmm6
	vfmadd213ss	.LC137(%rip), %xmm13, %xmm6
	vdivss	%xmm6, %xmm10, %xmm6
	vaddss	%xmm1, %xmm6, %xmm11
	vmulss	368(%rsp), %xmm11, %xmm10
	movq	352(%rsp), %rsi
	vdivss	%xmm11, %xmm1, %xmm1
	vsubss	%xmm12, %xmm1, %xmm13
	vfmadd132ss	%xmm10, %xmm12, %xmm13
	vmovss	.LC110(%rip), %xmm12
	vaddss	%xmm7, %xmm12, %xmm6
	vmovss	.LC143(%rip), %xmm12
	vmovss	%xmm13, (%r8,%rax,4)
	vmovss	(%rsi,%rax,4), %xmm11
	vmulss	.LC78(%rip), %xmm11, %xmm1
	vsubss	.LC246(%rip), %xmm7, %xmm13
	vmulss	%xmm1, %xmm6, %xmm10
	vmulss	(%r15,%rax,4), %xmm12, %xmm6
	vfmadd132ss	.LC141(%rip), %xmm10, %xmm13
	vminss	.LC145(%rip), %xmm6, %xmm1
	vaddss	.LC147(%rip), %xmm1, %xmm10
	vmulss	764(%rsp), %xmm10, %xmm6
	vdivss	%xmm10, %xmm1, %xmm12
	vsubss	%xmm11, %xmm12, %xmm1
	vmovss	.LC151(%rip), %xmm12
	vfmadd132ss	%xmm6, %xmm11, %xmm1
	vmovss	.LC149(%rip), %xmm11
	vaddss	%xmm7, %xmm11, %xmm10
	vmovss	%xmm1, (%rsi,%rax,4)
	vmulss	(%r14,%rax,4), %xmm12, %xmm1
	vfmadd213ss	516(%rsp), %xmm10, %xmm1
	vaddss	%xmm1, %xmm13, %xmm10
	vmovss	.LC153(%rip), %xmm13
	vmovss	.LC49(%rip), %xmm1
	vaddss	%xmm7, %xmm13, %xmm6
	vmulss	.LC155(%rip), %xmm6, %xmm11
	vminss	%xmm4, %xmm11, %xmm12
	vmaxss	%xmm3, %xmm12, %xmm13
	vmovss	.LC159(%rip), %xmm12
	vmovaps	%xmm13, %xmm11
	vfmadd132ss	%xmm0, %xmm2, %xmm11
	vroundss	$9, %xmm11, %xmm11, %xmm11
	vfmsub132ss	%xmm0, %xmm11, %xmm13
	vcvttss2sil	%xmm11, %ecx
	vfmadd213ss	.LC51(%rip), %xmm13, %xmm1
	vfmadd213ss	.LC53(%rip), %xmm13, %xmm1
	addl	$127, %ecx
	sall	$23, %ecx
	vmovd	%ecx, %xmm6
	vfmadd132ss	%xmm13, %xmm9, %xmm1
	vfmadd132ss	%xmm13, %xmm8, %xmm1
	vfmadd132ss	%xmm13, %xmm15, %xmm1
	vmovss	.LC157(%rip), %xmm13
	vfmadd132ss	%xmm7, %xmm12, %xmm13
	vmovss	.LC49(%rip), %xmm12
	vfmadd132ss	%xmm6, %xmm5, %xmm1
	vminss	%xmm4, %xmm13, %xmm11
	vmaxss	%xmm3, %xmm11, %xmm6
	vmovss	.LC161(%rip), %xmm11
	vdivss	%xmm1, %xmm5, %xmm1
	vmovaps	%xmm6, %xmm13
	vfmadd132ss	%xmm0, %xmm2, %xmm13
	vroundss	$9, %xmm13, %xmm13, %xmm13
	vfmsub132ss	%xmm0, %xmm13, %xmm6
	vcvttss2sil	%xmm13, %ecx
	vfmadd213ss	.LC51(%rip), %xmm6, %xmm12
	vfmadd213ss	.LC53(%rip), %xmm6, %xmm12
	addl	$127, %ecx
	sall	$23, %ecx
	vfmadd132ss	%xmm6, %xmm9, %xmm12
	vfmadd132ss	%xmm6, %xmm8, %xmm12
	vfmadd132ss	%xmm12, %xmm15, %xmm6
	vmovss	.LC163(%rip), %xmm12
	vfmadd132ss	%xmm7, %xmm12, %xmm11
	vminss	%xmm4, %xmm11, %xmm7
	vmovss	.LC49(%rip), %xmm11
	vmaxss	%xmm3, %xmm7, %xmm7
	vmovaps	%xmm7, %xmm12
	vfmadd132ss	%xmm0, %xmm2, %xmm12
	vroundss	$9, %xmm12, %xmm12, %xmm12
	vfmsub132ss	%xmm0, %xmm12, %xmm7
	vcvttss2sil	%xmm12, %esi
	vmovd	%ecx, %xmm12
	vfmadd213ss	.LC51(%rip), %xmm7, %xmm11
	vfmadd213ss	.LC53(%rip), %xmm7, %xmm11
	movq	744(%rsp), %rcx
	addl	$127, %esi
	sall	$23, %esi
	vmovd	%esi, %xmm13
	movq	536(%rsp), %rsi
	vfmadd132ss	%xmm7, %xmm9, %xmm11
	vfmadd132ss	%xmm7, %xmm8, %xmm11
	vfmadd132ss	%xmm7, %xmm15, %xmm11
	vmulss	%xmm13, %xmm11, %xmm7
	vsubss	(%r14,%rax,4), %xmm1, %xmm13
	vmovss	764(%rsp), %xmm11
	vmovss	864(%rsp), %xmm1
	vfmadd132ss	%xmm12, %xmm7, %xmm6
	vmovss	.LC167(%rip), %xmm7
	vmovss	372(%rsp), %xmm12
	vfmsub213ss	520(%rsp), %xmm1, %xmm12
	vfmadd132ss	.LC165(%rip), %xmm14, %xmm12
	vfmadd231ss	800(%rsp), %xmm7, %xmm12
	vmulss	%xmm11, %xmm6, %xmm6
	vfmadd213ss	(%r14,%rax,4), %xmm6, %xmm13
	vmovss	%xmm13, (%r14,%rax,4)
	vmovss	(%r15,%rax,4), %xmm13
	vmulss	.LC169(%rip), %xmm13, %xmm6
	vfmsub231ss	.LC171(%rip), %xmm14, %xmm6
	vaddss	%xmm12, %xmm10, %xmm14
	vmovss	832(%rsp), %xmm10
	vfnmadd132ss	%xmm11, %xmm1, %xmm14
	vfmadd132ss	%xmm11, %xmm13, %xmm6
	vmovss	%xmm6, (%r15,%rax,4)
	vmovss	%xmm10, (%rcx,%rax,4)
	movl	%edx, (%rsi,%rax,4)
	movq	752(%rsp), %rdx
	vmovss	%xmm14, (%rdx,%rax,4)
	addq	$1, %rax
	cmpl	%eax, 760(%rsp)
	jg	.L34
	jmp	.L30
	.p2align 4,,10
	.p2align 3
.L101:
	leal	-1(%r14), %r13d
	cmpl	$6, %r13d
	jbe	.L44
	movslq	736(%rsp), %rcx
	movslq	%r9d, %rbx
	movl	%r14d, %r8d
	vxorpd	%xmm1, %xmm1, %xmm1
	movq	752(%rsp), %rsi
	shrl	$3, %r8d
	addq	%rbx, %rcx
	salq	$5, %r8
	leaq	(%rsi,%rcx,4), %rdi
	leaq	(%r8,%rdi), %r12
	subq	$32, %r8
	shrq	$5, %r8
	addq	$1, %r8
	andl	$7, %r8d
	je	.L16
	cmpq	$1, %r8
	je	.L77
	cmpq	$2, %r8
	je	.L78
	cmpq	$3, %r8
	je	.L79
	cmpq	$4, %r8
	je	.L80
	cmpq	$5, %r8
	je	.L81
	cmpq	$6, %r8
	je	.L82
	vmovups	(%rdi), %ymm11
	vcvtps2pd	(%rdi), %ymm10
	addq	$32, %rdi
	vextractf128	$0x1, %ymm11, %xmm12
	vcvtps2pd	%xmm12, %ymm13
	vaddpd	%ymm13, %ymm10, %ymm1
.L82:
	vmovups	(%rdi), %ymm15
	vcvtps2pd	(%rdi), %ymm14
	addq	$32, %rdi
	vextractf128	$0x1, %ymm15, %xmm2
	vcvtps2pd	%xmm2, %ymm0
	vaddpd	%ymm0, %ymm14, %ymm3
	vaddpd	%ymm3, %ymm1, %ymm1
.L81:
	vmovups	(%rdi), %ymm4
	vcvtps2pd	(%rdi), %ymm6
	addq	$32, %rdi
	vextractf128	$0x1, %ymm4, %xmm5
	vcvtps2pd	%xmm5, %ymm7
	vaddpd	%ymm7, %ymm6, %ymm8
	vaddpd	%ymm8, %ymm1, %ymm1
.L80:
	vmovups	(%rdi), %ymm10
	vcvtps2pd	(%rdi), %ymm9
	addq	$32, %rdi
	vextractf128	$0x1, %ymm10, %xmm11
	vcvtps2pd	%xmm11, %ymm12
	vaddpd	%ymm12, %ymm9, %ymm13
	vaddpd	%ymm13, %ymm1, %ymm1
.L79:
	vmovups	(%rdi), %ymm15
	vcvtps2pd	(%rdi), %ymm14
	addq	$32, %rdi
	vextractf128	$0x1, %ymm15, %xmm2
	vcvtps2pd	%xmm2, %ymm0
	vaddpd	%ymm0, %ymm14, %ymm3
	vaddpd	%ymm3, %ymm1, %ymm1
.L78:
	vmovups	(%rdi), %ymm4
	vcvtps2pd	(%rdi), %ymm6
	addq	$32, %rdi
	vextractf128	$0x1, %ymm4, %xmm5
	vcvtps2pd	%xmm5, %ymm7
	vaddpd	%ymm7, %ymm6, %ymm8
	vaddpd	%ymm8, %ymm1, %ymm1
.L77:
	vmovups	(%rdi), %ymm10
	vcvtps2pd	(%rdi), %ymm9
	addq	$32, %rdi
	cmpq	%rdi, %r12
	vextractf128	$0x1, %ymm10, %xmm11
	vcvtps2pd	%xmm11, %ymm12
	vaddpd	%ymm12, %ymm9, %ymm13
	vaddpd	%ymm13, %ymm1, %ymm1
	je	.L94
.L16:
	vmovups	(%rdi), %ymm15
	vmovups	32(%rdi), %ymm5
	vcvtps2pd	(%rdi), %ymm14
	vcvtps2pd	32(%rdi), %ymm4
	vmovups	64(%rdi), %ymm12
	vcvtps2pd	64(%rdi), %ymm11
	addq	$256, %rdi
	vextractf128	$0x1, %ymm15, %xmm2
	vextractf128	$0x1, %ymm5, %xmm7
	vcvtps2pd	%xmm2, %ymm0
	vaddpd	%ymm0, %ymm14, %ymm3
	vcvtps2pd	%xmm7, %ymm8
	vaddpd	%ymm8, %ymm4, %ymm9
	vextractf128	$0x1, %ymm12, %xmm13
	vmovups	-128(%rdi), %ymm8
	vcvtps2pd	-128(%rdi), %ymm7
	vmovups	-160(%rdi), %ymm0
	vcvtps2pd	-160(%rdi), %ymm2
	vaddpd	%ymm3, %ymm1, %ymm6
	vcvtps2pd	%xmm13, %ymm1
	vaddpd	%ymm1, %ymm11, %ymm14
	vextractf128	$0x1, %ymm0, %xmm3
	vmovups	-96(%rdi), %ymm1
	vcvtps2pd	-96(%rdi), %ymm13
	vmovups	-64(%rdi), %ymm0
	vaddpd	%ymm9, %ymm6, %ymm10
	vcvtps2pd	%xmm3, %ymm6
	vaddpd	%ymm6, %ymm2, %ymm4
	vextractf128	$0x1, %ymm8, %xmm9
	vcvtps2pd	-64(%rdi), %ymm6
	vaddpd	%ymm14, %ymm10, %ymm15
	vcvtps2pd	%xmm9, %ymm10
	vaddpd	%ymm10, %ymm7, %ymm11
	vextractf128	$0x1, %ymm1, %xmm14
	vmovups	-32(%rdi), %ymm10
	vcvtps2pd	-32(%rdi), %ymm9
	cmpq	%rdi, %r12
	vaddpd	%ymm4, %ymm15, %ymm5
	vcvtps2pd	%xmm14, %ymm15
	vaddpd	%ymm15, %ymm13, %ymm2
	vextractf128	$0x1, %ymm0, %xmm4
	vaddpd	%ymm11, %ymm5, %ymm12
	vcvtps2pd	%xmm4, %ymm5
	vaddpd	%ymm5, %ymm6, %ymm7
	vextractf128	$0x1, %ymm10, %xmm11
	vaddpd	%ymm2, %ymm12, %ymm3
	vcvtps2pd	%xmm11, %ymm12
	vaddpd	%ymm12, %ymm9, %ymm13
	vaddpd	%ymm7, %ymm3, %ymm8
	vaddpd	%ymm13, %ymm8, %ymm1
	jne	.L16
.L94:
	vextractf128	$0x1, %ymm1, %xmm14
	movl	%r14d, %r9d
	movl	524(%rsp), %eax
	vaddpd	%xmm1, %xmm14, %xmm15
	andl	$-8, %r9d
	vaddpd	%xmm14, %xmm1, %xmm3
	cmpl	%r9d, %r14d
	leal	(%rax,%r9), %r10d
	vunpckhpd	%xmm15, %xmm15, %xmm2
	vaddpd	%xmm15, %xmm2, %xmm13
	je	.L104
	vzeroupper
.L15:
	movl	%r14d, %edx
	subl	%r9d, %edx
	leal	-1(%rdx), %r11d
	cmpl	$2, %r11d
	jbe	.L19
	movslq	736(%rsp), %r13
	movslq	512(%rsp), %rcx
	movl	%edx, %esi
	movq	752(%rsp), %rbx
	andl	$-4, %esi
	addq	%rcx, %r13
	addl	%esi, %r10d
	addq	%r9, %r13
	andl	$3, %edx
	vmovups	(%rbx,%r13,4), %xmm6
	vmovhps	%xmm6, 16(%rsp)
	vmovaps	16(%rsp), %xmm0
	vcvtps2pd	%xmm6, %xmm1
	vcvtps2pd	%xmm0, %xmm4
	vaddpd	%xmm4, %xmm1, %xmm5
	vaddpd	%xmm3, %xmm5, %xmm7
	vunpckhpd	%xmm7, %xmm7, %xmm8
	vaddpd	%xmm7, %xmm8, %xmm13
	je	.L14
.L19:
	movl	760(%rsp), %edx
	leal	1(%r10), %r9d
	movslq	%r10d, %r8
	vxorpd	%xmm9, %xmm9, %xmm9
	movq	752(%rsp), %rdi
	leaq	0(,%r8,4), %r12
	cmpl	%r9d, %edx
	vcvtss2sd	(%rdi,%r8,4), %xmm9, %xmm10
	vaddsd	%xmm10, %xmm13, %xmm13
	jle	.L14
	addl	$2, %r10d
	vcvtss2sd	4(%rdi,%r12), %xmm9, %xmm11
	vaddsd	%xmm11, %xmm13, %xmm13
	cmpl	%r10d, %edx
	jle	.L14
	vcvtss2sd	8(%rdi,%r12), %xmm9, %xmm12
	vaddsd	%xmm12, %xmm13, %xmm13
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L13:
	movl	$0, 736(%rsp)
	addl	$1, %r14d
	jmp	.L41
	.p2align 4,,10
	.p2align 3
.L103:
	vzeroupper
	jmp	.L30
	.p2align 4,,10
	.p2align 3
.L104:
	vzeroupper
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L44:
	movl	524(%rsp), %r10d
	vxorpd	%xmm3, %xmm3, %xmm3
	xorl	%r9d, %r9d
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L46:
	xorl	%edx, %edx
	jmp	.L27
.L45:
	movq	%rax, %r10
	jmp	.L21
	.cfi_endproc
.LFE59:
	.size	run_sim._omp_fn.0, .-run_sim._omp_fn.0
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC256:
	.string	"n_cells=%d steps=%d threads=%d  best=%.4fs  %.4f us/step  1s-brain=%.4f s  (Vs0[last]=%.3f)\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB58:
	.cfi_startproc
	endbr64
	leaq	8(%rsp), %r10
	.cfi_def_cfa 10, 0
	andq	$-32, %rsp
	pushq	-8(%r10)
	pushq	%rbp
	movq	%rsp, %rbp
	.cfi_escape 0x10,0x6,0x2,0x76,0
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%r10
	.cfi_escape 0xf,0x3,0x76,0x58,0x6
	.cfi_escape 0x10,0xf,0x2,0x76,0x78
	.cfi_escape 0x10,0xe,0x2,0x76,0x70
	.cfi_escape 0x10,0xd,0x2,0x76,0x68
	.cfi_escape 0x10,0xc,0x2,0x76,0x60
	pushq	%rbx
	subq	$384, %rsp
	.cfi_escape 0x10,0x3,0x2,0x76,0x50
	movq	%fs:40, %rax
	movq	%rax, -56(%rbp)
	xorl	%eax, %eax
	cmpl	$1, %edi
	jg	.L118
	movl	$100000, -404(%rbp)
	movl	$3000, %r13d
	movl	$3, %r14d
.L106:
	movslq	%r13d, %r8
	leaq	-368(%rbp), %rbx
	leaq	-240(%rbp), %r12
	leaq	0(,%r8,4), %r15
	movq	%r15, %rdi
	call	malloc@PLT
	movl	-404(%rbp), %esi
	movq	%rbx, %rdi
	movq	%rax, -400(%rbp)
	call	state_init.constprop.0
	movl	-368(%rbp), %eax
	movl	$200, %esi
	vmovq	-328(%rbp), %xmm6
	vmovq	-312(%rbp), %xmm2
	cmpl	%esi, %r13d
	vpinsrq	$1, -304(%rbp), %xmm2, %xmm4
	vxorps	%xmm2, %xmm2, %xmm2
	vmovq	-344(%rbp), %xmm5
	vmovq	-400(%rbp), %xmm3
	cmovle	%r13d, %esi
	movabsq	$5303949066, %rdx
	vpinsrq	$1, -320(%rbp), %xmm6, %xmm7
	movq	.LC252(%rip), %rcx
	movl	%eax, -92(%rbp)
	leaq	run_sim._omp_fn.0(%rip), %rdi
	vpinsrq	$1, -336(%rbp), %xmm5, %xmm0
	vmovq	-280(%rbp), %xmm10
	movq	%rdx, -108(%rbp)
	xorl	%edx, %edx
	vpinsrq	$1, -352(%rbp), %xmm3, %xmm1
	vinserti128	$0x1, %xmm4, %ymm7, %ymm9
	movq	%rcx, -100(%rbp)
	xorl	%ecx, %ecx
	vcvtsi2ssl	%eax, %xmm2, %xmm4
	vmovq	-296(%rbp), %xmm12
	vpinsrq	$1, -272(%rbp), %xmm10, %xmm11
	movl	%esi, -112(%rbp)
	vinserti128	$0x1, %xmm0, %ymm1, %ymm8
	vmovq	-248(%rbp), %xmm15
	movq	%r12, %rsi
	vpinsrq	$1, -288(%rbp), %xmm12, %xmm13
	vmovq	-264(%rbp), %xmm0
	vmovdqa	%ymm8, -240(%rbp)
	vpinsrq	$1, -360(%rbp), %xmm15, %xmm5
	vpinsrq	$1, -256(%rbp), %xmm0, %xmm3
	vinserti128	$0x1, %xmm11, %ymm13, %ymm14
	vmovdqa	%ymm9, -208(%rbp)
	vmovss	%xmm4, -88(%rbp)
	vinserti128	$0x1, %xmm5, %ymm3, %ymm1
	vmovdqa	%ymm14, -176(%rbp)
	vmovdqa	%ymm1, -144(%rbp)
	vzeroupper
	call	GOMP_parallel@PLT
	movq	%rbx, %rdi
	call	state_free
	testl	%r14d, %r14d
	jle	.L112
	movq	-400(%rbp), %rdi
	leaq	-384(%rbp), %r10
	vmovsd	.LC251(%rip), %xmm6
	xorl	%r11d, %r11d
	movq	%r10, -424(%rbp)
	leaq	-4(%rdi,%r15), %r9
	vmovsd	%xmm6, -392(%rbp)
	movl	%r14d, %r15d
	movl	%r11d, %r14d
	movq	%r9, -416(%rbp)
	.p2align 4,,10
	.p2align 3
.L108:
	movl	-404(%rbp), %esi
	movq	%rbx, %rdi
	call	state_init.constprop.0
	movq	-424(%rbp), %rsi
	movl	$1, %edi
	call	clock_gettime@PLT
	movl	-368(%rbp), %r8d
	xorl	%ecx, %ecx
	vmovq	-328(%rbp), %xmm15
	vmovq	-312(%rbp), %xmm13
	vmovq	-344(%rbp), %xmm7
	movabsq	$5303949066, %rax
	movl	%r13d, -112(%rbp)
	vpinsrq	$1, -320(%rbp), %xmm15, %xmm5
	vmovq	-400(%rbp), %xmm10
	movl	%r8d, -92(%rbp)
	movq	%r12, %rsi
	vpinsrq	$1, -304(%rbp), %xmm13, %xmm14
	vxorps	%xmm13, %xmm13, %xmm13
	vpinsrq	$1, -336(%rbp), %xmm7, %xmm9
	movq	%rax, -108(%rbp)
	movq	.LC252(%rip), %rdx
	vmovq	-280(%rbp), %xmm0
	leaq	run_sim._omp_fn.0(%rip), %rdi
	vpinsrq	$1, -352(%rbp), %xmm10, %xmm11
	vinserti128	$0x1, %xmm14, %ymm5, %ymm3
	vpinsrq	$1, -272(%rbp), %xmm0, %xmm2
	vcvtsi2ssl	%r8d, %xmm13, %xmm14
	vmovq	-296(%rbp), %xmm1
	movq	%rdx, -100(%rbp)
	xorl	%edx, %edx
	vinserti128	$0x1, %xmm9, %ymm11, %ymm12
	vmovq	-248(%rbp), %xmm6
	vpinsrq	$1, -288(%rbp), %xmm1, %xmm4
	vmovdqa	%ymm3, -208(%rbp)
	vmovq	-264(%rbp), %xmm7
	vmovdqa	%ymm12, -240(%rbp)
	vpinsrq	$1, -360(%rbp), %xmm6, %xmm9
	vpinsrq	$1, -256(%rbp), %xmm7, %xmm10
	vinserti128	$0x1, %xmm2, %ymm4, %ymm8
	vmovss	%xmm14, -88(%rbp)
	vinserti128	$0x1, %xmm9, %ymm10, %ymm11
	vmovdqa	%ymm8, -176(%rbp)
	vmovdqa	%ymm11, -144(%rbp)
	vzeroupper
	call	GOMP_parallel@PLT
	movq	%r12, %rsi
	addl	$1, %r14d
	movl	$1, %edi
	call	clock_gettime@PLT
	vxorpd	%xmm12, %xmm12, %xmm12
	movq	-232(%rbp), %rcx
	movq	-240(%rbp), %rsi
	subq	-376(%rbp), %rcx
	subq	-384(%rbp), %rsi
	movq	-416(%rbp), %rdi
	vcvtsi2sdq	%rcx, %xmm12, %xmm15
	vcvtsi2sdq	%rsi, %xmm12, %xmm5
	vfmadd132sd	.LC253(%rip), %xmm5, %xmm15
	vminsd	-392(%rbp), %xmm15, %xmm3
	vmovss	(%rdi), %xmm0
	movq	%rbx, %rdi
	vmovss	%xmm0, -408(%rbp)
	vmovsd	%xmm3, -392(%rbp)
	call	state_free
	cmpl	%r14d, %r15d
	jne	.L108
.L107:
	vxorpd	%xmm2, %xmm2, %xmm2
	vmovsd	-392(%rbp), %xmm4
	vcvtsi2sdl	%r13d, %xmm2, %xmm1
	vdivsd	%xmm1, %xmm4, %xmm8
	vmulsd	.LC254(%rip), %xmm8, %xmm6
	vmovsd	%xmm6, -416(%rbp)
	call	omp_get_max_threads@PLT
	vmovsd	-416(%rbp), %xmm1
	movl	%r13d, %ecx
	movl	$2, %edi
	movl	-404(%rbp), %edx
	vmulsd	.LC255(%rip), %xmm1, %xmm2
	movl	%eax, %r8d
	leaq	.LC256(%rip), %rsi
	vmovsd	-392(%rbp), %xmm0
	movl	$4, %eax
	vcvtss2sd	-408(%rbp), %xmm3, %xmm3
	call	__printf_chk@PLT
	movq	-400(%rbp), %rdi
	call	free@PLT
	movq	-56(%rbp), %rax
	subq	%fs:40, %rax
	jne	.L119
	addq	$384, %rsp
	xorl	%eax, %eax
	popq	%rbx
	popq	%r9
	.cfi_remember_state
	.cfi_def_cfa 10, 0
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	leaq	-8(%r9), %rsp
	.cfi_def_cfa 7, 8
	ret
.L118:
	.cfi_restore_state
	movl	%edi, %r14d
	movq	8(%rsi), %rdi
	movq	%rsi, %rbx
	movl	$10, %edx
	xorl	%esi, %esi
	call	strtol@PLT
	cmpl	$2, %r14d
	movl	%eax, -404(%rbp)
	je	.L111
	movq	16(%rbx), %rdi
	xorl	%esi, %esi
	movl	$10, %edx
	call	strtol@PLT
	cmpl	$3, %r14d
	movl	%eax, %r13d
	je	.L106
	movq	24(%rbx), %rdi
	movl	$10, %edx
	xorl	%esi, %esi
	call	strtol@PLT
	movl	%eax, %r14d
	jmp	.L106
.L111:
	movl	$3000, %r13d
	movl	$3, %r14d
	jmp	.L106
.L112:
	vmovsd	.LC251(%rip), %xmm8
	movl	$0x00000000, -408(%rbp)
	vmovsd	%xmm8, -392(%rbp)
	jmp	.L107
.L119:
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE58:
	.size	main, .-main
	.local	sigma.0
	.comm	sigma.0,8,8
	.section	.rodata.cst4,"aM",@progbits,4
	.align 4
.LC0:
	.long	1047449455
	.align 4
.LC1:
	.long	1074037636
	.align 4
.LC2:
	.long	1036831949
	.align 4
.LC3:
	.long	1060320051
	.align 4
.LC4:
	.long	904921088
	.align 4
.LC5:
	.long	-1031012352
	.align 4
.LC9:
	.long	1047702558
	.align 4
.LC15:
	.long	864026624
	.align 4
.LC16:
	.long	814313567
	.align 4
.LC17:
	.long	-1073741824
	.align 4
.LC18:
	.long	885592027
	.align 4
.LC21:
	.long	1128792064
	.align 4
.LC22:
	.long	1129447424
	.align 4
.LC23:
	.long	1051372203
	.align 4
.LC24:
	.long	1059760811
	.set	.LC25,.LC135
	.section	.rodata.cst32,"aM",@progbits,32
	.align 32
.LC26:
	.long	1042062492
	.long	1042062492
	.long	1042062492
	.long	1042062492
	.long	1042062492
	.long	1042062492
	.long	1042062492
	.long	1042062492
	.set	.LC27,.LC26
	.align 32
.LC28:
	.long	1057300152
	.long	1057300152
	.long	1057300152
	.long	1057300152
	.long	1057300152
	.long	1057300152
	.long	1057300152
	.long	1057300152
	.set	.LC29,.LC28
	.set	.LC31,.LC174
	.align 32
.LC32:
	.long	-1024458752
	.long	-1024458752
	.long	-1024458752
	.long	-1024458752
	.long	-1024458752
	.long	-1024458752
	.long	-1024458752
	.long	-1024458752
	.set	.LC33,.LC32
	.align 32
.LC34:
	.long	998445679
	.long	998445679
	.long	998445679
	.long	998445679
	.long	998445679
	.long	998445679
	.long	998445679
	.long	998445679
	.set	.LC35,.LC34
	.align 32
.LC36:
	.long	1114898432
	.long	1114898432
	.long	1114898432
	.long	1114898432
	.long	1114898432
	.long	1114898432
	.long	1114898432
	.long	1114898432
	.set	.LC37,.LC36
	.align 32
.LC38:
	.long	-1099706562
	.long	-1099706562
	.long	-1099706562
	.long	-1099706562
	.long	-1099706562
	.long	-1099706562
	.long	-1099706562
	.long	-1099706562
	.set	.LC39,.LC38
	.align 32
.LC40:
	.long	1118830592
	.long	1118830592
	.long	1118830592
	.long	1118830592
	.long	1118830592
	.long	1118830592
	.long	1118830592
	.long	1118830592
	.set	.LC41,.LC40
	.align 32
.LC42:
	.long	-1028784128
	.long	-1028784128
	.long	-1028784128
	.long	-1028784128
	.long	-1028784128
	.long	-1028784128
	.long	-1028784128
	.long	-1028784128
	.set	.LC43,.LC42
	.align 32
.LC44:
	.long	1069066811
	.long	1069066811
	.long	1069066811
	.long	1069066811
	.long	1069066811
	.long	1069066811
	.long	1069066811
	.long	1069066811
	.set	.LC45,.LC44
	.align 32
.LC46:
	.long	1056964608
	.long	1056964608
	.long	1056964608
	.long	1056964608
	.long	1056964608
	.long	1056964608
	.long	1056964608
	.long	1056964608
	.set	.LC47,.LC46
	.align 32
.LC48:
	.long	989206731
	.long	989206731
	.long	989206731
	.long	989206731
	.long	989206731
	.long	989206731
	.long	989206731
	.long	989206731
	.set	.LC49,.LC48
	.align 32
.LC50:
	.long	1007896582
	.long	1007896582
	.long	1007896582
	.long	1007896582
	.long	1007896582
	.long	1007896582
	.long	1007896582
	.long	1007896582
	.set	.LC51,.LC50
	.align 32
.LC52:
	.long	1030038116
	.long	1030038116
	.long	1030038116
	.long	1030038116
	.long	1030038116
	.long	1030038116
	.long	1030038116
	.long	1030038116
	.set	.LC53,.LC52
	.section	.rodata.cst4
	.align 4
.LC55:
	.long	1047915220
	.align 4
.LC57:
	.long	1060205179
	.set	.LC59,.LC188
	.set	.LC62,.LC190
	.section	.rodata.cst32
	.align 32
.LC63:
	.long	1118437376
	.long	1118437376
	.long	1118437376
	.long	1118437376
	.long	1118437376
	.long	1118437376
	.long	1118437376
	.long	1118437376
	.set	.LC64,.LC63
	.align 32
.LC65:
	.long	1039200497
	.long	1039200497
	.long	1039200497
	.long	1039200497
	.long	1039200497
	.long	1039200497
	.long	1039200497
	.long	1039200497
	.set	.LC66,.LC65
	.align 32
.LC67:
	.long	1126170624
	.long	1126170624
	.long	1126170624
	.long	1126170624
	.long	1126170624
	.long	1126170624
	.long	1126170624
	.long	1126170624
	.set	.LC68,.LC67
	.align 32
.LC69:
	.long	1023969417
	.long	1023969417
	.long	1023969417
	.long	1023969417
	.long	1023969417
	.long	1023969417
	.long	1023969417
	.long	1023969417
	.set	.LC70,.LC69
	.align 32
.LC71:
	.long	1101004800
	.long	1101004800
	.long	1101004800
	.long	1101004800
	.long	1101004800
	.long	1101004800
	.long	1101004800
	.long	1101004800
	.set	.LC72,.LC71
	.align 32
.LC73:
	.long	1118306304
	.long	1118306304
	.long	1118306304
	.long	1118306304
	.long	1118306304
	.long	1118306304
	.long	1118306304
	.long	1118306304
	.set	.LC74,.LC73
	.align 32
.LC75:
	.long	1040991779
	.long	1040991779
	.long	1040991779
	.long	1040991779
	.long	1040991779
	.long	1040991779
	.long	1040991779
	.long	1040991779
	.set	.LC76,.LC75
	.set	.LC78,.LC198
	.align 32
.LC79:
	.long	1106247680
	.long	1106247680
	.long	1106247680
	.long	1106247680
	.long	1106247680
	.long	1106247680
	.long	1106247680
	.long	1106247680
	.set	.LC80,.LC79
	.align 32
.LC81:
	.long	-1103483252
	.long	-1103483252
	.long	-1103483252
	.long	-1103483252
	.long	-1103483252
	.long	-1103483252
	.long	-1103483252
	.long	-1103483252
	.set	.LC82,.LC81
	.align 32
.LC83:
	.long	1116471296
	.long	1116471296
	.long	1116471296
	.long	1116471296
	.long	1116471296
	.long	1116471296
	.long	1116471296
	.long	1116471296
	.set	.LC84,.LC83
	.align 32
.LC85:
	.long	1043369277
	.long	1043369277
	.long	1043369277
	.long	1043369277
	.long	1043369277
	.long	1043369277
	.long	1043369277
	.long	1043369277
	.set	.LC86,.LC85
	.align 32
.LC87:
	.long	1125515264
	.long	1125515264
	.long	1125515264
	.long	1125515264
	.long	1125515264
	.long	1125515264
	.long	1125515264
	.long	1125515264
	.set	.LC88,.LC87
	.align 32
.LC89:
	.long	1109393408
	.long	1109393408
	.long	1109393408
	.long	1109393408
	.long	1109393408
	.long	1109393408
	.long	1109393408
	.long	1109393408
	.set	.LC90,.LC89
	.align 32
.LC91:
	.long	-1124581872
	.long	-1124581872
	.long	-1124581872
	.long	-1124581872
	.long	-1124581872
	.long	-1124581872
	.long	-1124581872
	.long	-1124581872
	.set	.LC92,.LC91
	.align 32
.LC93:
	.long	1077936128
	.long	1077936128
	.long	1077936128
	.long	1077936128
	.long	1077936128
	.long	1077936128
	.long	1077936128
	.long	1077936128
	.set	.LC94,.LC93
	.align 32
.LC95:
	.long	-1110651699
	.long	-1110651699
	.long	-1110651699
	.long	-1110651699
	.long	-1110651699
	.long	-1110651699
	.long	-1110651699
	.long	-1110651699
	.set	.LC96,.LC95
	.align 32
.LC97:
	.long	1112014848
	.long	1112014848
	.long	1112014848
	.long	1112014848
	.long	1112014848
	.long	1112014848
	.long	1112014848
	.long	1112014848
	.set	.LC98,.LC97
	.align 32
.LC99:
	.long	982622900
	.long	982622900
	.long	982622900
	.long	982622900
	.long	982622900
	.long	982622900
	.long	982622900
	.long	982622900
	.set	.LC100,.LC99
	.align 32
.LC101:
	.long	1111228416
	.long	1111228416
	.long	1111228416
	.long	1111228416
	.long	1111228416
	.long	1111228416
	.long	1111228416
	.long	1111228416
	.set	.LC102,.LC101
	.align 32
.LC103:
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.set	.LC104,.LC103
	.align 32
.LC105:
	.long	1091567616
	.long	1091567616
	.long	1091567616
	.long	1091567616
	.long	1091567616
	.long	1091567616
	.long	1091567616
	.long	1091567616
	.set	.LC106,.LC105
	.align 32
.LC107:
	.long	-1034158080
	.long	-1034158080
	.long	-1034158080
	.long	-1034158080
	.long	-1034158080
	.long	-1034158080
	.long	-1034158080
	.long	-1034158080
	.set	.LC108,.LC107
	.set	.LC110,.LC214
	.align 32
.LC111:
	.long	1103626240
	.long	1103626240
	.long	1103626240
	.long	1103626240
	.long	1103626240
	.long	1103626240
	.long	1103626240
	.long	1103626240
	.set	.LC112,.LC111
	.align 32
.LC113:
	.long	1040522936
	.long	1040522936
	.long	1040522936
	.long	1040522936
	.long	1040522936
	.long	1040522936
	.long	1040522936
	.long	1040522936
	.set	.LC114,.LC113
	.align 32
.LC115:
	.long	-1135817523
	.long	-1135817523
	.long	-1135817523
	.long	-1135817523
	.long	-1135817523
	.long	-1135817523
	.long	-1135817523
	.long	-1135817523
	.set	.LC116,.LC115
	.align 32
.LC117:
	.long	1071141356
	.long	1071141356
	.long	1071141356
	.long	1071141356
	.long	1071141356
	.long	1071141356
	.long	1071141356
	.long	1071141356
	.set	.LC118,.LC117
	.align 32
.LC119:
	.long	1114636288
	.long	1114636288
	.long	1114636288
	.long	1114636288
	.long	1114636288
	.long	1114636288
	.long	1114636288
	.long	1114636288
	.set	.LC120,.LC119
	.align 32
.LC121:
	.long	1131413504
	.long	1131413504
	.long	1131413504
	.long	1131413504
	.long	1131413504
	.long	1131413504
	.long	1131413504
	.long	1131413504
	.set	.LC122,.LC121
	.align 32
.LC123:
	.long	1063116253
	.long	1063116253
	.long	1063116253
	.long	1063116253
	.long	1063116253
	.long	1063116253
	.long	1063116253
	.long	1063116253
	.set	.LC124,.LC123
	.align 32
.LC125:
	.long	1015222895
	.long	1015222895
	.long	1015222895
	.long	1015222895
	.long	1015222895
	.long	1015222895
	.long	1015222895
	.long	1015222895
	.set	.LC126,.LC125
	.align 32
.LC127:
	.long	1083179008
	.long	1083179008
	.long	1083179008
	.long	1083179008
	.long	1083179008
	.long	1083179008
	.long	1083179008
	.long	1083179008
	.set	.LC128,.LC127
	.align 32
.LC129:
	.long	1033066128
	.long	1033066128
	.long	1033066128
	.long	1033066128
	.long	1033066128
	.long	1033066128
	.long	1033066128
	.long	1033066128
	.set	.LC130,.LC129
	.align 32
.LC131:
	.long	1071225242
	.long	1071225242
	.long	1071225242
	.long	1071225242
	.long	1071225242
	.long	1071225242
	.long	1071225242
	.long	1071225242
	.set	.LC132,.LC131
	.align 32
.LC133:
	.long	1091043328
	.long	1091043328
	.long	1091043328
	.long	1091043328
	.long	1091043328
	.long	1091043328
	.long	1091043328
	.long	1091043328
	.set	.LC134,.LC133
	.align 32
.LC135:
	.long	1045220557
	.long	1045220557
	.long	1045220557
	.long	1045220557
	.long	1045220557
	.long	1045220557
	.long	1045220557
	.long	1045220557
	.align 32
.LC136:
	.long	-1082130432
	.long	-1082130432
	.long	-1082130432
	.long	-1082130432
	.long	-1082130432
	.long	-1082130432
	.long	-1082130432
	.long	-1082130432
	.set	.LC137,.LC136
	.align 32
.LC138:
	.long	1017370378
	.long	1017370378
	.long	1017370378
	.long	1017370378
	.long	1017370378
	.long	1017370378
	.long	1017370378
	.long	1017370378
	.set	.LC139,.LC138
	.align 32
.LC140:
	.long	1014694077
	.long	1014694077
	.long	1014694077
	.long	1014694077
	.long	1014694077
	.long	1014694077
	.long	1014694077
	.long	1014694077
	.set	.LC141,.LC140
	.align 32
.LC142:
	.long	933741996
	.long	933741996
	.long	933741996
	.long	933741996
	.long	933741996
	.long	933741996
	.long	933741996
	.long	933741996
	.set	.LC143,.LC142
	.align 32
.LC144:
	.long	1008981770
	.long	1008981770
	.long	1008981770
	.long	1008981770
	.long	1008981770
	.long	1008981770
	.long	1008981770
	.long	1008981770
	.set	.LC145,.LC144
	.align 32
.LC146:
	.long	1014350479
	.long	1014350479
	.long	1014350479
	.long	1014350479
	.long	1014350479
	.long	1014350479
	.long	1014350479
	.long	1014350479
	.set	.LC147,.LC146
	.align 32
.LC148:
	.long	1110179840
	.long	1110179840
	.long	1110179840
	.long	1110179840
	.long	1110179840
	.long	1110179840
	.long	1110179840
	.long	1110179840
	.set	.LC149,.LC148
	.align 32
.LC150:
	.long	1039516303
	.long	1039516303
	.long	1039516303
	.long	1039516303
	.long	1039516303
	.long	1039516303
	.long	1039516303
	.long	1039516303
	.set	.LC151,.LC150
	.align 32
.LC152:
	.long	1117782016
	.long	1117782016
	.long	1117782016
	.long	1117782016
	.long	1117782016
	.long	1117782016
	.long	1117782016
	.long	1117782016
	.set	.LC153,.LC152
	.align 32
.LC154:
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.long	1048576000
	.set	.LC155,.LC154
	.section	.rodata.cst4
	.align 4
.LC157:
	.long	-1112530747
	.section	.rodata.cst32
	.align 32
.LC158:
	.long	-1050044006
	.long	-1050044006
	.long	-1050044006
	.long	-1050044006
	.long	-1050044006
	.long	-1050044006
	.long	-1050044006
	.long	-1050044006
	.set	.LC159,.LC158
	.section	.rodata.cst4
	.align 4
.LC161:
	.long	1032805417
	.section	.rodata.cst32
	.align 32
.LC162:
	.long	-1074832343
	.long	-1074832343
	.long	-1074832343
	.long	-1074832343
	.long	-1074832343
	.long	-1074832343
	.long	-1074832343
	.long	-1074832343
	.set	.LC163,.LC162
	.align 32
.LC164:
	.long	1028443341
	.long	1028443341
	.long	1028443341
	.long	1028443341
	.long	1028443341
	.long	1028443341
	.long	1028443341
	.long	1028443341
	.set	.LC165,.LC164
	.align 32
.LC166:
	.long	1043430987
	.long	1043430987
	.long	1043430987
	.long	1043430987
	.long	1043430987
	.long	1043430987
	.long	1043430987
	.long	1043430987
	.set	.LC167,.LC166
	.align 32
.LC168:
	.long	1033476506
	.long	1033476506
	.long	1033476506
	.long	1033476506
	.long	1033476506
	.long	1033476506
	.long	1033476506
	.long	1033476506
	.set	.LC169,.LC168
	.align 32
.LC170:
	.long	-1069547520
	.long	-1069547520
	.long	-1069547520
	.long	-1069547520
	.long	-1069547520
	.long	-1069547520
	.long	-1069547520
	.long	-1069547520
	.set	.LC171,.LC170
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC174:
	.long	-1054867456
	.long	-1054867456
	.long	-1054867456
	.long	-1054867456
	.set	.LC175,.LC32
	.align 16
.LC188:
	.long	1065353203
	.long	1065353203
	.long	1065353203
	.long	1065353203
	.align 16
.LC190:
	.long	1065353216
	.long	1065353216
	.long	1065353216
	.long	1065353216
	.align 16
.LC198:
	.long	1108082688
	.long	1108082688
	.long	1108082688
	.long	1108082688
	.set	.LC199,.LC79
	.set	.LC200,.LC81
	.set	.LC202,.LC85
	.set	.LC204,.LC89
	.set	.LC205,.LC91
	.set	.LC207,.LC95
	.set	.LC211,.LC103
	.align 16
.LC214:
	.long	1117126656
	.long	1117126656
	.long	1117126656
	.long	1117126656
	.set	.LC215,.LC111
	.set	.LC216,.LC113
	.set	.LC217,.LC115
	.set	.LC218,.LC117
	.section	.rodata.cst4
	.align 4
.LC246:
	.long	1092616192
	.align 4
.LC247:
	.long	1123024896
	.align 4
.LC248:
	.long	1113325568
	.section	.rodata.cst16
	.align 16
.LC249:
	.long	-2147483648
	.long	0
	.long	0
	.long	0
	.section	.rodata.cst4
	.align 4
.LC250:
	.long	127
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC251:
	.long	966823146
	.long	1177108057
	.align 8
.LC252:
	.long	1073741824
	.long	1065353216
	.align 8
.LC253:
	.long	-400107883
	.long	1041313291
	.align 8
.LC254:
	.long	0
	.long	1093567616
	.align 8
.LC255:
	.long	-1717986919
	.long	1069128089
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
