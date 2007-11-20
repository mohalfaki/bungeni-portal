/*
 * generalEditorPanel4.java
 *
 * Created on September 8, 2007, 4:49 PM
 */

package org.bungeni.editor.panels;

import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.net.URL;
import java.util.HashMap;
import java.util.Vector;
import javax.swing.AbstractAction;
import javax.swing.DefaultListModel;
import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JPopupMenu;
import javax.swing.JTree;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeCellRenderer;
import javax.swing.tree.TreePath;
import org.bungeni.db.BungeniClientDB;
import org.bungeni.db.DefaultInstanceFactory;
import org.bungeni.db.QueryResults;
import org.bungeni.db.SettingsQueryFactory;
import org.bungeni.editor.actions.EditorActionFactory;
import org.bungeni.editor.actions.IEditorActionEvent;
import org.bungeni.editor.actions.toolbarAction;
import org.bungeni.editor.selectors.SelectorDialogModes;
import org.bungeni.ooo.OOComponentHelper;
import org.bungeni.utils.CommonTreeFunctions;

/**
 *
 * @author  Administrator
 */
public class generalEditorPanel4 extends templatePanel implements ICollapsiblePanel , ActionListener {

    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(generalEditorPanel4.class.getName());
    private OOComponentHelper ooDocument;    
    private BungeniClientDB instance;
    
    private DefaultMutableTreeNode root;
  //  private DefaultMutableTreeNode[] visibleActionRoots;
    private JPopupMenu popupMenu;
    
    private  enum PopupTypeIdentifier {CREATE_EDIT , APPLY_MARKUP, EDIT  };
 
    private HashMap<PopupTypeIdentifier, String> popupMap = new HashMap<PopupTypeIdentifier, String>();
    
    /** Creates new form generalEditorPanel4 */
    public generalEditorPanel4() {
        log.debug("in constructor initComponents");
        initComponents();
        log.debug("in constructor initOthers");
        initOthers();
        log.debug("in constructor initTree");
        initTree();
        
        
     }
    
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {
        generalEditorScrollPane = new javax.swing.JScrollPane();
        treeGeneralEditor = new javax.swing.JTree();

        treeGeneralEditor.setFont(new java.awt.Font("Tahoma", 0, 12));
        generalEditorScrollPane.setViewportView(treeGeneralEditor);

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(generalEditorScrollPane, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 216, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(generalEditorScrollPane, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 235, Short.MAX_VALUE)
        );
    }// </editor-fold>//GEN-END:initComponents
    private void initOthers(){
        instance = new BungeniClientDB (DefaultInstanceFactory.DEFAULT_INSTANCE(), DefaultInstanceFactory.DEFAULT_DB());
        popupMenu = new JPopupMenu();
        
        popupMap.put(PopupTypeIdentifier.APPLY_MARKUP, "Apply Markup");
        popupMap.put(PopupTypeIdentifier.CREATE_EDIT, "Create Section");
        popupMap.put(PopupTypeIdentifier.EDIT, "Edit Section");
        
    }
    
    private void initTree() {
        toolbarAction rootAction = new toolbarAction("rootAction");
        toolbarAction inivisibleRoot = new toolbarAction("invisibleRootAction");
        
        root = new DefaultMutableTreeNode(inivisibleRoot);
        DefaultMutableTreeNode editorToolsRoot = new DefaultMutableTreeNode(rootAction);
        root.add(editorToolsRoot);
        
        log.debug("in InitTree");
        if (instance.Connect()) {
            log.debug("about to call createTreeNodes()");
            //create editor tools nodes
            createTreeNodes( editorToolsRoot, true);
            //createToolNodes(rootNode, rootAction, instance );
            instance.EndConnect();
        } 
        log.debug("after createTreeNodes()");
        treeGeneralEditor.setModel(new DefaultTreeModel(root));
        treeGeneralEditor.addMouseListener(new treeGeneralEditorMouseListener());
        treeGeneralEditor.setCellRenderer(new treeGeneralEditorCellRenderer());
        CommonTreeFunctions.expandAll(treeGeneralEditor, true);
        treeGeneralEditor.setRootVisible(false);
    }
    
    private void createTreeNodes(DefaultMutableTreeNode rootNode, boolean recurse) {
        try {
        toolbarAction baseNode = (toolbarAction) rootNode.getUserObject();
        String actionParent = baseNode.action_name();
        //HashMap results = new HashMap();
        Vector<Vector<String>> resultRows = new Vector<Vector<String>>();
       // Vector<Vector> results = new Vector<Vector>();
        //DefaultMutableTreeNode child = new DefaultMutableTreeNode (addThisActionObject);
        
        //addToThisNode.add( child);
        QueryResults query_results;
        if (actionParent.equals("parent"))
            query_results = instance.QueryResults(SettingsQueryFactory.Q_FETCH_PARENT_ACTIONS());
        else
            query_results = instance.QueryResults(SettingsQueryFactory.Q_FETCH_PARENT_ACTIONS(actionParent));
        
        //QueryResults query_results = instance.QueryResults(SettingsQueryFactory.Q_FETCH_CHILD_TOOLBAR_ACTIONS(actionParent));
        //QueryResults query_results = new QueryResults(results);
        if (query_results == null) 
            return ;
        
        if (query_results.hasResults() ) {
             HashMap columns = query_results.columnNameMap();
             //child actions are present
             //call the result nodes recursively...
             resultRows = query_results.theResults();
             //toolbarActionGroup grp = new toolbarActionGroup("create a section", "create a section");
                 for (int i = 0 ; i < resultRows.size(); i++ ) {
                   //get the results row by row into a string vector
                   Vector<java.lang.String> tableRow = new Vector<java.lang.String>();
                   tableRow = resultRows.elementAt(i);
                   toolbarAction action = new toolbarAction(tableRow, columns );
                   DefaultMutableTreeNode node = new DefaultMutableTreeNode(action);
                   rootNode.add(node);
                   if (recurse ) {
                       createTreeNodes(node, true);
                   }
               }
        }
        } catch (Exception ex) {
            log.error("Exception in createTreeNodes: " + ex.getMessage());
            ex.printStackTrace();
        }
      return ;
    }
    
    public void setOOComponentHandle(OOComponentHelper ooComponent) {
        ooDocument = ooComponent;
    }

    public Component getObjectHandle() {
        return this;
    }

    public IEditorActionEvent getEventClass(toolbarAction action) {
        IEditorActionEvent event = EditorActionFactory.getEventClass(action);
        return event;
    }

    public void setParentWindowHandle(Component c) {
    }

    public void actionPerformed(ActionEvent e) {
    }
    
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JScrollPane generalEditorScrollPane;
    private javax.swing.JTree treeGeneralEditor;
    // End of variables declaration//GEN-END:variables
    
    
    class treePopupMenuAction extends AbstractAction {
        PopupTypeIdentifier treePopupMenuAction_popupType;
        
        public treePopupMenuAction (toolbarAction action) {
            super(action.toString());
            putValue("USER_OBJECT", action);
        }
        
        public treePopupMenuAction (String actionText,  toolbarAction action, PopupTypeIdentifier id ) {
            
            super(actionText);
            putValue("POPUP_IDENTIFIER", id);
            putValue("USER_OBJECT", action);
            treePopupMenuAction_popupType = id;
            
            
        }
        
        public void actionPerformed(ActionEvent e) {
            //toolbarAction action = (toolbarAction) e.getSource();
            //System.out.println("action = " + action.toString());
               String s = ( "    Event source: " + e.getSource()
                  + "\n");
                log.debug("popup, actionPerforemd : "+ s);
               Object value = this.getValue("USER_OBJECT");
               Object popId = this.getValue("POPUP_IDENTIFIER");
               if (value != null ) {
                   log.debug("popup, actionPerforemd : popupSelection");
                
                   processPopupSelection();
               }
        }

        private SelectorDialogModes getDialogMode(){
            if (!ooDocument.isTextSelected()) {
                if ( treePopupMenuAction_popupType == PopupTypeIdentifier.CREATE_EDIT) {
                    return SelectorDialogModes.TEXT_INSERTION;
                }
                if (treePopupMenuAction_popupType ==  PopupTypeIdentifier.EDIT){
                    return SelectorDialogModes.TEXT_EDIT;
                }
                
                return SelectorDialogModes.NONE;
                
            } else {
                return SelectorDialogModes.TEXT_SELECTED;
            }
        }     
        private void processPopupSelection(){
            //get selction path
              TreePath path = treeGeneralEditor.getSelectionPath();
              //get current node selected...
              DefaultMutableTreeNode thisNode = (DefaultMutableTreeNode) path.getLastPathComponent();
              if (treePopupMenuAction_popupType == PopupTypeIdentifier.CREATE_EDIT) {
                    toolbarAction action =(toolbarAction)thisNode.getUserObject();
                    /** commented for issue 108 ***
                    if (!ooDocument.isTextSelected())
                        action.setSelectorDialogMode(SelectorDialogModes.TEXT_INSERTION);
                    else
                        action.setSelectorDialogMode(SelectorDialogModes.TEXT_SELECTED);
                     */
                    action.setSelectorDialogMode(this.getDialogMode());
                    IEditorActionEvent event = getEventClass(action);
                    event.doCommand(ooDocument, action);
              } else
               if (treePopupMenuAction_popupType == PopupTypeIdentifier.EDIT) {
                    //look for existing masthead section 
                    //if it exists popup the edit screen for it.
                    toolbarAction action =(toolbarAction)thisNode.getUserObject();
                    //we look for sections matching this action type.
                    action.setSelectorDialogMode(this.getDialogMode());
                    IEditorActionEvent event = getEventClass(action);
                    event.doCommand(ooDocument, action);
               }
              /*else 
              if (popupType == PopupTypeIdentifier.VIEW_ACTIONS) {
                   if (thisNode.isLeaf()) {
                      log.debug("processPopupSelection : thisNode = leaf");
                    instance.Connect();
                    createTreeNodes(thisNode, false);
                    instance.EndConnect();
                    if (!thisNode.isLeaf()) {
                     treeGeneralEditor.expandPath(path);
                    } 
                  }
              }*/ else 
              if (treePopupMenuAction_popupType == PopupTypeIdentifier.APPLY_MARKUP) {
                    toolbarAction action =(toolbarAction)thisNode.getUserObject();
                    action.setSelectorDialogMode(this.getDialogMode());
                    IEditorActionEvent event = getEventClass(action);
                    event.doCommand(ooDocument, action);
              }
                //get toolbar action     
              //toolbarAction action = (toolbarAction) thisNode.getUserObject();
              //add items only if it is a leaf node

        }
        
 
    }
    

    
    class treeGeneralEditorMouseListener implements MouseListener {
        public void mouseClicked(MouseEvent evt) {
      
        }
        
       private void createPopupMenuItems (toolbarAction baseNodeAction){
           
            if (baseNodeAction.action_type().equals("section")) {
                popupMenu.removeAll();
                //popupMenu.add(new treePopupMenuAction(popup_section_actions[0], baseNodeAction, PopupTypeIdentifier.VIEW_ACTIONS));
                popupMenu.add(new treePopupMenuAction(popupMap.get(PopupTypeIdentifier.CREATE_EDIT), baseNodeAction, PopupTypeIdentifier.CREATE_EDIT));
                if (baseNodeAction.action_edit_dlg_allowed() == 1)
                    popupMenu.add(new treePopupMenuAction(popupMap.get(PopupTypeIdentifier.EDIT), baseNodeAction, PopupTypeIdentifier.EDIT));
                //popupMenu.add(new treePopupMenuAction(popup_section_actions[2]))
            } else 
            if (baseNodeAction.action_type().equals("markup")) {
                popupMenu.removeAll();
                popupMenu.add(new treePopupMenuAction(popupMap.get(PopupTypeIdentifier.APPLY_MARKUP), baseNodeAction, PopupTypeIdentifier.APPLY_MARKUP));
            }
         }
        public void mousePressed(MouseEvent evt) {
                  int selRow = treeGeneralEditor.getRowForLocation(evt.getX(), evt.getY());
                TreePath selPath = treeGeneralEditor.getPathForLocation(evt.getX(), evt.getY());
                // TreePath selPath = treeGeneralEditor.getSelectionPath();
                 //DefaultMutableTreeNode node = (DefaultMutableTreeNode) selPath.getLastPathComponent();
                 if (selRow != -1 ) {
                 //if (node != null ) {     
              
                     if (evt.getClickCount() == 1) {
                         
                         DefaultMutableTreeNode node = (DefaultMutableTreeNode) selPath.getLastPathComponent();
                         System.out.println("node = "+ (toolbarAction) node.getUserObject());   
                         toolbarAction action = (toolbarAction)node.getUserObject();
                         createPopupMenuItems (action);
                         popupMenu.show(evt.getComponent(), evt.getX(), evt.getY());
                      return;
                     }  
                
                 }
        }

        public void mouseReleased(MouseEvent e) {
        }

        public void mouseEntered(MouseEvent e) {
        }

        public void mouseExited(MouseEvent e) {
        }
        
    }

class treeGeneralEditorCellRenderer extends JLabel implements TreeCellRenderer {
        
        ImageIcon[] imgIcons;
         int SECTION_ICON = 0;
         int SECTION_PLUS_ICON = 1;
         int MARKUP_ICON = 2;
        String[] icons = { "action_m.png", "action_m_plus.png", "action_s.png" };
        
        public treeGeneralEditorCellRenderer() {
              imgIcons = new ImageIcon[icons.length];
              for (int i=0; i < imgIcons.length ; i++) {
                  String imgPath = "/gui/" + icons[i] ;
                    URL imgUrl = null;
                  imgUrl = getClass().getResource(imgPath);
                  imgIcons[i] = new ImageIcon(imgUrl, "");
              }
        }

        public Component getTreeCellRendererComponent(JTree tree, Object value, boolean selected, boolean expanded, boolean leaf, int row, boolean hasFocus) {
                setText(" "+ value.toString( ));
                if (selected) {
                  setOpaque(true);
                }
                else {
                  setOpaque(false);
                }

                if (value instanceof DefaultMutableTreeNode) {
                  DefaultMutableTreeNode uo = (DefaultMutableTreeNode)value;
                  if (uo.isLeaf()) {
                      toolbarAction act = (toolbarAction) uo.getUserObject();
                      if (act.action_type().equals("markup")) 
                        setIcon(imgIcons[MARKUP_ICON]);
                      else 
                        setIcon(imgIcons[SECTION_ICON]);
                  } else {
                      setIcon(imgIcons[SECTION_PLUS_ICON]);
                  }
                }
                return this;    
                }
    }    



}
