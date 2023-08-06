#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/stat.h>
#include <linux/pid.h>
#include <linux/sched.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Franciszek Piszcz");

static int pid = 0;
static struct task_struct * task = NULL;

module_param(pid, int, 0);

int init_module(void) {
  if(!pid) {
    printk(KERN_ALERT "signal_unkillable: Please specify pid of the process you want to make unkillable.\n");
    return -1;
  }
  task = pid_task(find_get_pid(pid), PIDTYPE_PID);
  if(task) {
    printk(KERN_INFO "signal_unkillable: Setting SIGNAL_UNKILLABLE for %d\n", pid);
    task->signal->flags = task->signal->flags | SIGNAL_UNKILLABLE;
  } else {
    printk(KERN_ALERT "signal_unkillable: Error getting task_struct for pid %d\n", pid);
    return -1;
  }
  return 0;
}

void cleanup_module(void) {}
